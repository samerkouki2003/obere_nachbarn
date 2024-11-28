import streamlit as st

# Basisklasse für Konzepte
class Concept:
    def __str__(self):
        return ""

# Klasse für einen einfachen Konzeptnamen
class ConceptName(Concept):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

# Klasse für eine Konjunktion
class Conjunction(Concept):
    def __init__(self, *concepts):
        self.concepts = concepts

    def __str__(self):
        return " ⊓ ".join(str(concept) for concept in self.concepts)

# Klasse für eine existenzielle Restriktion
class ExistentialRestriction(Concept):
    def __init__(self, role, filler):
        self.role = role
        self.filler = filler

    def __str__(self):
        return f"∃{self.role}.({self.filler})"

# Berechnung der oberen Nachbarn
def compute_upper_neighbors(concept):
    if isinstance(concept, ConceptName):
        return []
    if isinstance(concept, Conjunction):
        upper_neighbors = []
        for conjunct in concept.concepts:
            new_concepts = [c for c in concept.concepts if c != conjunct]
            if isinstance(conjunct, ExistentialRestriction):
                upper_filler_neighbors = compute_upper_neighbors(conjunct.filler)
                for upper_filler in upper_filler_neighbors:
                    new_concepts.append(ExistentialRestriction(conjunct.role, upper_filler))
            if new_concepts:
                upper_neighbors.append(Conjunction(*new_concepts))
        return upper_neighbors
    if isinstance(concept, ExistentialRestriction):
        upper_filler_neighbors = compute_upper_neighbors(concept.filler)
        return [ExistentialRestriction(concept.role, upper_filler) for upper_filler in upper_filler_neighbors]
    return []

# Rekursive Konzept-Erstellung
def create_concept(unique_id=""):
    concept_type = st.radio(
        "Wählen Sie den Konzepttyp:",
        ["Konzeptname", "Existenzielle Restriktion", "Konjunktion"],
        key=f"concept_type_{unique_id}"
    )
    if concept_type == "Konzeptname":
        name = st.text_input(
            "Name des Konzepts (z.B. A, B):",
            key=f"concept_name_{unique_id}"
        )
        if name:
            return ConceptName(name)

    elif concept_type == "Existenzielle Restriktion":
        role = st.text_input(
            "Rolle der Restriktion (z.B. r):",
            key=f"role_{unique_id}"
        )
        if role:
            st.write("Erstellen Sie den Füller:")
            filler = create_concept(unique_id=f"{unique_id}_filler")
            if filler:
                return ExistentialRestriction(role, filler)

    elif concept_type == "Konjunktion":
        num_concepts = st.number_input(
            "Anzahl der Konzepte in der Konjunktion:",
            min_value=1, step=1,
            key=f"num_concepts_{unique_id}"
        )
        conjuncts = []
        for i in range(int(num_concepts)):
            st.write(f"Erstellen Sie Konzept {i + 1}:")
            conjunct = create_concept(unique_id=f"{unique_id}_conjunct_{i}")
            if conjunct:
                conjuncts.append(conjunct)
        return Conjunction(*conjuncts)

    return None

# Hauptanwendung
st.title("Konzept-Builder mit oberen Nachbarn")
st.header("Konzept erstellen")

main_concept = create_concept(unique_id="main")

if main_concept:
    st.subheader("Erstelltes Konzept")
    st.write(main_concept)

    st.header("Obere Nachbarn berechnen")
    if st.button("Berechnen"):
        upper_neighbors = compute_upper_neighbors(main_concept)
        if upper_neighbors:
            st.subheader("Obere Nachbarn:")
            for neighbor in upper_neighbors:
                st.write(neighbor)
        else:
            st.write("Keine oberen Nachbarn gefunden.")

###############################################################################################

import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st

def visualize_neighbors_centered(original_concept, neighbors):
    """
    Visualisiert ein Konzept und seine oberen Nachbarn als nach oben gerichteten Graph,
    wobei das Originalkonzept in der Mitte liegt.
    """
    G = nx.DiGraph()  # Direktgerichteter Graph

    # Originalknoten hinzufügen
    original_label = str(original_concept)
    G.add_node(original_label)

    # Obere Nachbarn hinzufügen und mit dem Original verbinden
    neighbor_labels = []
    for i, neighbor in enumerate(neighbors):
        neighbor_label = f"{neighbor}"
        neighbor_labels.append(neighbor_label)
        G.add_node(neighbor_label)
        G.add_edge(original_label, neighbor_label)

    # Manuelles Layout: Originalknoten in der Mitte unten, Nachbarn oben
    pos = {}
    pos[original_label] = (0, 0)  # Originalknoten in der Mitte (x=0, y=0)

    # Nachbarn symmetrisch oberhalb platzieren
    num_neighbors = len(neighbor_labels)
    for i, neighbor_label in enumerate(neighbor_labels):
        x_offset = (i - (num_neighbors - 1) / 2)  # Symmetrische Verteilung entlang der x-Achse
        pos[neighbor_label] = (x_offset, 1)  # Nachbarn auf einer höheren Ebene

    # Graph zeichnen
    fig, ax = plt.subplots(figsize=(10, 6))  # Größe des Diagramms
    nx.draw(
        G, pos, with_labels=True, node_size=3000, node_color="lightblue", 
        font_size=10, font_weight="bold", arrowsize=20, ax=ax
    )
    st.pyplot(fig)  # Diagramm in Streamlit anzeigen

# Streamlit-App
def main():
    st.title("Visualisierung der oberen Nachbarn")
    
    # Eingabe des Originalkonzepts
    original_concept = st.text_input("Gib das Originalkonzept ein (z.B. 'A')", "Originalkonzept")
    
    # Berechnung der oberen Nachbarn (Dummy-Funktion, hier mit Beispieldaten)
    neighbors = compute_upper_neighbors(original_concept)  # Passe diese Funktion an deine Logik an
    
    if st.button("Visualisierung anzeigen"):
        if neighbors:
            st.write(f"Originalkonzept: {original_concept}")
            st.write(f"Obere Nachbarn: {neighbors}")
            visualize_neighbors_centered(original_concept, neighbors)
        else:
            st.write("Keine Nachbarn gefunden.")

# Dummy-Funktion zur Berechnung der Nachbarn (ersetzen durch eigene Logik)
def compute_upper_neighbors(concept):
    # Beispiel: Rückgabe von Dummy-Nachbarn
    return ["Nachbar 1", "Nachbar 2", "Nachbar 3"]

if __name__ == "__main__":
    main()
