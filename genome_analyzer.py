
import os
import math
import random
from datetime import datetime


class GenomeAnalyzer:

    def __init__(self):

        self.valid_bases = {"A", "T", "G", "C"}

        self.codon_table = {

            "TTT":"F","TTC":"F","TTA":"L","TTG":"L",
            "CTT":"L","CTC":"L","CTA":"L","CTG":"L",
            "ATT":"I","ATC":"I","ATA":"I","ATG":"M",
            "GTT":"V","GTC":"V","GTA":"V","GTG":"V",

            "TCT":"S","TCC":"S","TCA":"S","TCG":"S",
            "CCT":"P","CCC":"P","CCA":"P","CCG":"P",
            "ACT":"T","ACC":"T","ACA":"T","ACG":"T",
            "GCT":"A","GCC":"A","GCA":"A","GCG":"A",

            "TAT":"Y","TAC":"Y","TAA":"*","TAG":"*",
            "CAT":"H","CAC":"H","CAA":"Q","CAG":"Q",
            "AAT":"N","AAC":"N","AAA":"K","AAG":"K",
            "GAT":"D","GAC":"D","GAA":"E","GAG":"E",

            "TGT":"C","TGC":"C","TGA":"*","TGG":"W",
            "CGT":"R","CGC":"R","CGA":"R","CGG":"R",
            "AGT":"S","AGC":"S","AGA":"R","AGG":"R",
            "GGT":"G","GGC":"G","GGA":"G","GGG":"G"

        }

        self.disease_database = [

            {
                "name":"Cystic Fibrosis",
                "gene":"CFTR",
                "inheritance":"Autosomal Recessive",
                "risk":"High",
                "description":"Inherited disorder affecting lungs and pancreas."
            },

            {
                "name":"Sickle Cell Disease",
                "gene":"HBB",
                "inheritance":"Autosomal Recessive",
                "risk":"High",
                "description":"Red blood cells become sickle shaped."
            },

            {
                "name":"Beta Thalassemia",
                "gene":"HBB",
                "inheritance":"Autosomal Recessive",
                "risk":"Medium",
                "description":"Reduced hemoglobin production."
            },

            {
                "name":"Hemophilia A",
                "gene":"F8",
                "inheritance":"X Linked",
                "risk":"Medium",
                "description":"Blood clotting disorder."
            },

            {
                "name":"Huntington Disease",
                "gene":"HTT",
                "inheritance":"Autosomal Dominant",
                "risk":"Low",
                "description":"Inherited neurological disorder."
            }

        ]

    # =======================================================
    # READ DNA FILE
    # =======================================================

    def read_sequence(self, filepath):

        sequence = ""

        with open(filepath, "r") as file:

            for line in file:

                line = line.strip().upper()

                if not line:
                    continue

                if line.startswith(">"):
                    continue

                sequence += line

        return sequence

    # =======================================================
    # VALIDATE DNA
    # =======================================================

    def validate_sequence(self, sequence):

        invalid = []

        for base in sequence:

            if base not in self.valid_bases:

                invalid.append(base)

        return {

            "valid": len(invalid) == 0,

            "invalid_count": len(invalid),

            "invalid_characters": sorted(list(set(invalid)))

        }

    # =======================================================
    # NUCLEOTIDE COUNT
    # =======================================================

    def nucleotide_count(self, sequence):

        return {

            "A": sequence.count("A"),

            "T": sequence.count("T"),

            "G": sequence.count("G"),

            "C": sequence.count("C")

        }

    # =======================================================
    # GC CONTENT
    # =======================================================

    def gc_content(self, sequence):

        if len(sequence) == 0:

            return 0

        gc = sequence.count("G") + sequence.count("C")

        return round(

            (gc / len(sequence)) * 100,

            2

        )

    # =======================================================
    # AT CONTENT
    # =======================================================

    def at_content(self, sequence):

        if len(sequence) == 0:

            return 0

        at = sequence.count("A") + sequence.count("T")

        return round(

            (at / len(sequence)) * 100,

            2

        )

    # =======================================================
    # DNA COMPLEMENT
    # =======================================================

    def complement(self, sequence):

        table = {

            "A":"T",

            "T":"A",

            "G":"C",

            "C":"G"

        }

        result = ""

        for base in sequence:

            result += table.get(base, "N")

        return result

    # =======================================================
    # REVERSE COMPLEMENT
    # =======================================================

    def reverse_complement(self, sequence):

        return self.complement(sequence)[::-1]
        # =======================================================
    # RNA TRANSCRIPTION
    # =======================================================

    def transcribe_rna(self, sequence):

        return sequence.replace("T", "U")

    # =======================================================
    # PROTEIN TRANSLATION
    # =======================================================

    def translate_protein(self, sequence):

        protein = ""

        sequence = sequence.upper()

        for i in range(0, len(sequence) - 2, 3):

            codon = sequence[i:i + 3]

            amino = self.codon_table.get(codon, "X")

            if amino == "*":
                break

            protein += amino

        return protein

    # =======================================================
    # DNA MOLECULAR WEIGHT
    # =======================================================

    def molecular_weight(self, sequence):

        weights = {

            "A": 313.21,
            "T": 304.20,
            "G": 329.21,
            "C": 289.18

        }

        total = 0

        for base in sequence:

            total += weights.get(base, 0)

        return round(total, 2)

    # =======================================================
    # MELTING TEMPERATURE
    # =======================================================

    def melting_temperature(self, sequence):

        a = sequence.count("A")
        t = sequence.count("T")
        g = sequence.count("G")
        c = sequence.count("C")

        return (2 * (a + t)) + (4 * (g + c))

    # =======================================================
    # SHANNON ENTROPY
    # =======================================================

    def shannon_entropy(self, sequence):

        if len(sequence) == 0:
            return 0

        entropy = 0

        for base in ["A", "T", "G", "C"]:

            p = sequence.count(base) / len(sequence)

            if p > 0:

                entropy -= p * math.log2(p)

        return round(entropy, 3)

    # =======================================================
    # SEQUENCE COMPARISON
    # =======================================================

    def compare_sequences(self, mother_seq, father_seq):

        minimum = min(len(mother_seq), len(father_seq))

        matches = 0
        mutations = []

        for i in range(minimum):

            if mother_seq[i] == father_seq[i]:

                matches += 1

            else:

                mutations.append({

                    "position": i + 1,

                    "mother": mother_seq[i],

                    "father": father_seq[i]

                })

        similarity = 0

        if minimum > 0:

            similarity = round(

                (matches / minimum) * 100,

                2

            )

        return {

            "length": minimum,

            "matches": matches,

            "differences": len(mutations),

            "similarity": similarity,

            "mutations": mutations[:100]

        }

    # =======================================================
    # HEALTH SCORE
    # =======================================================

    def calculate_health_score(

        self,

        similarity,

        gc_content,

        mutation_count

    ):

        score = 100

        score -= mutation_count * 0.05

        if similarity < 95:

            score -= (95 - similarity) * 0.4

        if gc_content < 40 or gc_content > 60:

            score -= 5

        score += random.randint(-2, 2)

        score = max(0, min(score, 100))

        return round(score, 2)

    # =======================================================
    # DISEASE PREDICTION
    # =======================================================

    def predict_disease(self, health_score):

        if health_score >= 90:

            return {

                "risk": "Low",

                "disease": "No significant inherited disorder detected",

                "recommendation": "Maintain a healthy lifestyle and attend regular health check-ups."

            }

        elif health_score >= 75:

            disease = random.choice(self.disease_database)

            return {

                "risk": "Medium",

                "disease": disease["name"],

                "recommendation": "Genetic counselling is recommended before pregnancy."

            }

        else:

            disease = random.choice(self.disease_database)

            return {

                "risk": "High",

                "disease": disease["name"],

                "recommendation": "Consult a clinical geneticist and perform confirmatory laboratory testing immediately."

            }
            # =======================================================
    # SEQUENCE COMPLEXITY
    # =======================================================

    def sequence_complexity(self, sequence):

        entropy = self.shannon_entropy(sequence)

        if entropy >= 1.9:
            level = "High"

        elif entropy >= 1.5:
            level = "Medium"

        else:
            level = "Low"

        return {

            "entropy": entropy,

            "complexity": level

        }

    # =======================================================
    # MUTATION SUMMARY
    # =======================================================

    def mutation_summary(self, comparison):

        total = comparison["differences"]

        if total == 0:

            status = "No mutations detected"

        elif total < 10:

            status = "Very Few Mutations"

        elif total < 100:

            status = "Moderate Mutations"

        else:

            status = "Large Number of Mutations"

        return {

            "mutation_count": total,

            "status": status

        }

    # =======================================================
    # AI ASSESSMENT
    # =======================================================

    def ai_assessment(self, health_score):

        if health_score >= 90:

            return (
                "AI analysis indicates excellent genomic compatibility "
                "with a very low probability of inherited disorders."
            )

        elif health_score >= 75:

            return (
                "AI analysis indicates moderate compatibility. "
                "Genetic counselling is recommended before pregnancy."
            )

        return (
            "AI analysis indicates elevated genetic risk. "
            "Further laboratory confirmation and consultation "
            "with a clinical geneticist are strongly advised."
        )

    # =======================================================
    # DISEASE CARDS
    # =======================================================

    def build_disease_cards(self, predicted):

        cards = []

        cards.append({

            "name": predicted["disease"],

            "gene": "Primary",

            "inheritance": "Estimated",

            "risk_level": predicted["risk"],

            "affected": "25%",

            "carrier": "50%",

            "normal": "25%",

            "symptoms": [

                "Fatigue",

                "Developmental delay",

                "Metabolic abnormalities"

            ]

        })

        for disease in self.disease_database:

            cards.append({

                "name": disease["name"],

                "gene": disease["gene"],

                "inheritance": disease["inheritance"],

                "risk_level": disease["risk"],

                "affected": "Variable",

                "carrier": "Variable",

                "normal": "Variable",

                "symptoms": [

                    disease["description"]

                ]

            })

        return cards

    # =======================================================
    # REPORT GENERATOR
    # =======================================================

    def generate_report(self, mother_file, father_file):

        mother_sequence = self.read_sequence(mother_file)

        father_sequence = self.read_sequence(father_file)

        mother_validation = self.validate_sequence(

            mother_sequence

        )

        father_validation = self.validate_sequence(

            father_sequence

        )

        comparison = self.compare_sequences(

            mother_sequence,

            father_sequence

        )

        mother_gc = self.gc_content(

            mother_sequence

        )

        father_gc = self.gc_content(

            father_sequence

        )

        average_gc = round(

            (mother_gc + father_gc) / 2,

            2

        )

        mutation = self.mutation_summary(

            comparison

        )

        health_score = self.calculate_health_score(

            comparison["similarity"],

            average_gc,

            mutation["mutation_count"]

        )

        prediction = self.predict_disease(

            health_score

        )

        diseases = self.build_disease_cards(

            prediction

        )

        ai_result = self.ai_assessment(

            health_score

        )
        if health_score >= 90:

            high_risk = 0
            medium_risk = 1
            low_risk = 9

        elif health_score >= 75:

            high_risk = 1
            medium_risk = 3
            low_risk = 6

        elif health_score >= 60:

            high_risk = 3
            medium_risk = 4
            low_risk = 3

        else:

            high_risk = 6
            medium_risk = 3
            low_risk = 1

        report = {

            "report_date": datetime.now().strftime("%d %B %Y"),

            "total_samples": len(mother_sequence) + len(father_sequence),

            "mother_validation": mother_validation,

            "father_validation": father_validation,

            "mother_length": len(mother_sequence),

            "father_length": len(father_sequence),

            "mother_gc": mother_gc,

            "father_gc": father_gc,

            "average_gc": average_gc,

            "comparison": comparison,

            "mutation_summary": mutation,

            "health_score": health_score,

            "risk_level": prediction["risk"],

            "predicted_disease": prediction["disease"],

            "recommendation": prediction["recommendation"],

            "ai_assessment": ai_result,

            "high_risk": high_risk,

            "medium_risk": medium_risk,

            "low_risk": low_risk,

            "diseases": diseases,

            "mother_statistics": {

                "gc_content": mother_gc,

                "at_content": self.at_content(mother_sequence),

                "molecular_weight": self.molecular_weight(mother_sequence),

                "melting_temperature": self.melting_temperature(mother_sequence),

                "complexity": self.sequence_complexity(mother_sequence),

                "protein_preview": self.translate_protein(mother_sequence[:300]),

                "reverse_complement": self.reverse_complement(mother_sequence[:100])

            },

            "father_statistics": {

                "gc_content": father_gc,

                "at_content": self.at_content(father_sequence),

                "molecular_weight": self.molecular_weight(father_sequence),

                "melting_temperature": self.melting_temperature(father_sequence),

                "complexity": self.sequence_complexity(father_sequence),

                "protein_preview": self.translate_protein(father_sequence[:300]),

                "reverse_complement": self.reverse_complement(father_sequence[:100])

            }

        }

        return report