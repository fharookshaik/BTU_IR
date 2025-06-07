# python main.py
# This file is a part of Information Retreival system that allows users to interact with parsed documents and search for relevant information based on user queries.

from document import Document
from my_module import load_collection_from_url, remove_stop_words, remove_stop_words_by_frequency, linear_boolean_search
import re
import os

class TerminalUI:
    """
        Terminal based User Interface for an Information Retreival system
            
        Provide interactive options to:
        - Download and parse story collections from a URL
        - View parsed documents
        - Perform linear boolean search on documents
        - Apply stopword filtering using a file or frequency-based method

        """
    def __init__(self):
        """
        Initialize the TerminalUI instance

        Attributes:
            inputs (dict): Store paramenters entereb by user
            documents (list): Stores parsed Documents objects
        """
        self.inputs = {}
        self.documents = []

    def run(self):
        """
        Run the main menu loop for user interaction.
        Displays a menu and handles user input for different functionalities.
        """
        while True:
            print("\n=== Information Retrieval System ===")
            print("1. 📥 Download & Parse Story Collection")
            print("2. 📚 View Parsed Documents")
            print("3. 🔍 Search Documents")
            print("4. 🛑 Stop Word Removal")
            print("5. ❌ Exit")

            choice = input("Select an action (1–5): ").strip()

            if choice == '1':
                self.download_and_parse()
            elif choice == '2':
                self.view_documents()
            elif choice == '3':
                self.search_documents()
            elif choice == '4':
                self.stopword_removal()
            elif choice == '5':
                print("Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter a number from 1 to 5.")

    def download_and_parse(self):
        """
        Prompt the user for parsing options and load documents from a given URL.

        Collects:
            - URL of the text source
            - Start and end lines for reading
            - Regex pattern for splitting stories
            - Author and origin metadata

        Updates:
            self.documents with parsed Document objects.
        """
        print("\n--- Download & Parse ---")

        self.inputs['url'] = input("Source URL: ").strip()

        while True:
            try:
                self.inputs['start_line'] = int(input("Start line (e.g., 50): ").strip())
                break
            except ValueError:
                print("❌ Please enter a valid integer.")

        end_line_input = input("End line (leave blank to read till end): ").strip()
        self.inputs['end_line'] = int(end_line_input) if end_line_input.isdigit() else None

        while True:
            pattern_input = input("Story Separator / Search Pattern (regex): ").strip()
            try:
                self.inputs['search_pattern'] = re.compile(pattern_input, re.DOTALL)
                break
            except re.error as e:
                print(f"❌ Invalid regex: {e}. Try again.")

        self.inputs['author'] = input("Author name: ").strip()
        self.inputs['origin'] = input("Book/source origin: ").strip()

        try:
            self.documents = load_collection_from_url(
                url=self.inputs['url'],
                author=self.inputs['author'],
                origin=self.inputs['origin'],
                start_line=self.inputs['start_line'],
                end_line=self.inputs['end_line'],
                search_pattern=self.inputs['search_pattern']
            )
            print(f"\n✅ Parsed {len(self.documents)} documents.")
        except Exception as e:
            print(f"❌ Error during parsing: {e}")

    def view_documents(self):
        """
        Display a summary of parsed documents.

        Allows the user to view the full raw text of a selected document by entering its ID.
        """
        if not self.documents:
            print("\n⚠️ No documents parsed yet.")
            return

        print("\n📚 Documents:")
        for doc in self.documents:
            print(f" - {doc}")

        doc_id_input = input("Enter document ID to view full text (or press Enter to skip): ").strip()
        if doc_id_input.isdigit():
            doc_id = int(doc_id_input)
            if 0 <= doc_id < len(self.documents):
                doc = self.documents[doc_id]
                print(f"\n--- {doc.title} ---")
                print(doc.raw_text)
            else:
                print("❌ Invalid document ID.")
        elif doc_id_input:
            print("❌ Please enter a valid numeric ID.")

    def search_documents(self):
        """
        Perform a linear boolean search over the parsed documents.

        Prompts the user for a search term and displays matching documents along with relevance scores.
        """
        if not self.documents:
            print("\n⚠️ Please parse documents first.")
            return

        term = input("\nEnter a search term: ").strip().lower()
        if not term:
            print("❌ Search term cannot be empty.")
            return

        try:
            results = linear_boolean_search(term=term, collection=self.documents, stopword_filtered=False)
            print(f"\n🔍 Results for '{term}': {len(results)} found.")
            print(f'- Doc_ID : Relevance Score')
            for score, doc in results:
                print(f" - {doc} : {score}")
        except Exception as e:
            print(f"❌ Error during search: {e}")

    def stopword_removal(self):
        """
        Perform stopword filtering on document terms.

        Offers two options:
            1. Use an external or internal stopword file.
            2. Use frequency-based filtering with user-defined thresholds.

        Updates each document's `filtered_terms` attribute.
        """
        if not self.documents:
            print("\n⚠️ Please parse documents first.")
            return

        while True:
            method = input("\nChoose method: (1) Stopword File or (2) Frequency-based: ").strip()
            if method in {'1', '2'}:
                break
            print("❌ Invalid option. Enter 1 or 2.")

        if method == '1':
            stop_file = input("Enter stopword file path (or press Enter to use internal list): ").strip()

            stopwords = None
            if stop_file:
                if os.path.exists(stop_file):
                    with open(stop_file, 'r') as f:
                        stopwords = set(word.strip().lower() for word in f)
                    print("✅ Stopword file loaded.")
                else:
                    print("❌ File not found. Using internal stopwords.")

            for doc in self.documents:
                doc.filtered_terms = remove_stop_words(terms=doc.terms, stopwords=stopwords)
            print("✅ Stopword filtering complete.")

        elif method == '2':
            while True:
                try:
                    common_freq = float(input("Enter Common Frequency (e.g., 0.5): ").strip())
                    rare_freq = float(input("Enter Rare Frequency (e.g., 0.1): ").strip())
                    if not (0 <= rare_freq <= 1 and 0 <= common_freq <= 1):
                        raise ValueError
                    break
                except ValueError:
                    print("❌ Please enter valid frequencies between 0 and 1.")

            for doc in self.documents:
                doc.filtered_terms = remove_stop_words_by_frequency(
                    terms=doc.terms,
                    collection=self.documents,
                    low_freq=rare_freq,
                    high_freq=common_freq
                )
            print("✅ Frequency-based stopword removal applied.")

        doc_id_input = input("Enter document ID to view filtered terms (or press Enter to skip): ").strip()
        if doc_id_input.isdigit():
            doc_id = int(doc_id_input)
            if 0 <= doc_id < len(self.documents):
                doc = self.documents[doc_id]
                print(f"\n--- {doc} ---")
                print(doc.filtered_terms)
            else:
                print("❌ Invalid document ID.")
        elif doc_id_input:
            print("❌ Please enter a valid numeric ID.")


# Run the terminal UI
if __name__ == "__main__":
    TerminalUI().run()
