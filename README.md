## nucleotide sequence Search Tool

A web application that allows users to perform BLAT searches on nucleotide sequences and retrieve gene information based on chromosome positions.

### About the Project

The BLAT Search Tool provides an easy-to-use interface for searching nucleotide sequences against the human genome. It retrieves relevant genomic data, including gene names, based on user-provided sequences and specified genome builds (GRCh37 or GRCh38).

### Technologies Used

Python: Backend logic using Flask framework.
Flask: Web framework for building the application.
Bootstrap: Frontend framework for styling and responsive design.
UCSC Genome Browser API: For performing BLAT searches and retrieving genomic data.
Ensembl REST API: For fetching gene names based on chromosome positions.
Getting Started

### Prerequisites

To run this project locally, ensure you have the following installed:

Python 3.x
pip (Python package installer)
Installation

### Clone the repository:
https://github.com/jaannawaz/Sequence-Search-Tool.git


Run the application: bash python app.py

Open your web browser and navigate to http://localhost:5000.

Usage Enter a nucleotide sequence of at least 20 base pairs in the input field. Select the appropriate genome build (GRCh37 or GRCh38). Click "Find Region" to perform the BLAT search. View the results displayed in a structured table format. Results

###  The results will show:

Chromosome number Start and end positions Strand information Number of matches and mismatches Percentage identity Gene names associated with the given positions

###  License

This project is licensed under the MIT License - see the LICENSE.md file for details.

### Acknowledgements

UCSC Genome Browser for providing genomic data APIs. Ensembl for their REST API services. Bootstrap for responsive design components. text
