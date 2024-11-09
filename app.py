import requests
from flask import Flask, render_template, request

app = Flask(__name__)

def blat_search(sequence, seq_type, genome="hg38"):
    url = "https://genome.ucsc.edu/cgi-bin/hgBlat"
    params = {
        "userSeq": sequence,
        "type": seq_type,
        "db": genome,
        "output": "json"
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            return None
    return None

def get_gene_name(chromosome, position):
    # Query Ensembl REST API for gene information
    server = "https://rest.ensembl.org"
    ext = f"/overlap/region/human/{chromosome}:{position}-{position}"
    headers = {"Content-Type": "application/json"}
    
    # Get genes
    genes_response = requests.get(f"{server}{ext}?feature=gene", headers=headers)
    genes = genes_response.json() if genes_response.ok else []
    
    # Return gene names or "Not Available"
    if genes:
        return ", ".join([g.get('external_name', 'N/A') for g in genes])
    
    return "Not Available"

def parse_blat_results(results):
    if isinstance(results, dict) and 'blat' in results:
        parsed_results = []
        for hit in results['blat']:
            chromosome = hit[13]
            chromosome_start = hit[15]
            chromosome_end = hit[16]

            # Try to get gene name using start position first
            gene_name_start = get_gene_name(chromosome, chromosome_start)
            # If not found, try using end position
            gene_name_end = get_gene_name(chromosome, chromosome_end) if gene_name_start == "Not Available" else gene_name_start

            parsed_hit = {
                "matches": hit[0],
                "misMatches": hit[1],
                "strand": hit[8],
                "chromosome": chromosome,
                "chromosome_start": chromosome_start,
                "chromosome_end": chromosome_end,
                "identity_percentage": (hit[0] / (hit[0] + hit[1])) * 100,
                "gene_name": gene_name_end  # Add gene name to parsed results
            }
            parsed_results.append(parsed_hit)
        
        return parsed_results
    
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sequence = request.form['sequence'].upper()
        build = request.form['build']
        
        if len(sequence) < 20:
            return render_template('index.html', error="Sequence must be at least 20 base pairs long.")
        
        genome = "hg19" if build == "GRCh37" else "hg38"
        
        # Determine sequence type
        if all(base in 'ATCG' for base in sequence):
            seq_type = "DNA"
        else:
            return render_template('index.html', error="Invalid sequence. Please check your input.")
        
        results = blat_search(sequence, seq_type, genome)
        
        if results is None:
            return render_template('index.html', error="Error fetching results from UCSC.")
        
        parsed_results = parse_blat_results(results)
        
        return render_template('results.html', results=parsed_results)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)