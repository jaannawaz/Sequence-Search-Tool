import requests
from bs4 import BeautifulSoup

def blat_search(sequence, genome="hg38"):
    url = "https://genome.ucsc.edu/cgi-bin/hgBlat"
    params = {
        "userSeq": sequence,
        "type": "DNA",
        "genome": genome,
        "output": "hyperlink"
    }
    
    response = requests.post(url, data=params)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for row in soup.find_all('tr')[1:]:  # Skip header row
            cols = row.find_all('td')
            if len(cols) >= 10:
                result = {
                    "score": cols[0].text.strip(),
                    "start": cols[2].text.strip(),
                    "end": cols[3].text.strip(),
                    "qsize": cols[4].text.strip(),
                    "identity": cols[5].text.strip(),
                    "chromosome": cols[8].text.strip(),
                    "strand": cols[9].text.strip(),
                    "start_genome": cols[10].text.strip(),
                    "end_genome": cols[11].text.strip(),
                }
                results.append(result)
        return results
    else:
        return None

# Example usage
sequence = "CTTGTTCTGCTAGGACCCTGGTTAGGAGTAGAATGGGACAATCCCGAGAGAGGAAAGCATGA"
results = blat_search(sequence)
print(results)