from collections import defaultdict
from owlready2 import get_ontology, sync_reasoner_pellet


def analyze_ontology(ontology):
    class_population = defaultdict(list)

    for owl_class in ontology.classes():
        excluded_classes = ['Domain_entity', 'Independent_entity', 'Value']
        if owl_class.name not in excluded_classes:
            instances_count = len(owl_class.instances())
            class_population[owl_class].append(instances_count)

    average_population = {owl_class: sum(population) / len(population) for owl_class, population in class_population.items()}

    max_population_class = max(average_population, key=average_population.get)
    min_population_class = min(average_population, key=average_population.get)

    print("Average Population for Each Class:")
    for owl_class, avg in average_population.items():
        print(f"The average number of individuals in {owl_class.name}: {avg:.0f}")

    print(f"\nClass with the Highest Average Population: {max_population_class.name}")
    print(f"Class with the Lowest Average Population: {min_population_class.name}")

    get_cv_info(ontology)


def get_cv_info(ontology):
    print("\nInformation about CV instances:")
    for cv_instance in ontology.individuals():
        print(f"\nCV Instance: {cv_instance.name}")
        print(f"Class: {cv_instance.__class__.name}")

        for prop in cv_instance.get_properties():
            values = getattr(cv_instance, prop.name)
            if values:
                if isinstance(values, list):
                    if len(values) > 1:
                        print(f"{prop.name}: {', '.join(str(value) for value in values)}")
                    else:
                        print(f"{prop.name}: {values[0]}")
                else:
                    print(f"{prop.name}: {values}")
            else:
                print(f"{prop.name}: Not specified")

        print("No CV Class specified.")


def check_ontology(rdf_file_path, property_name):
    ontology = get_ontology(rdf_file_path).load()

    sync_reasoner_pellet([ontology])

    num_classes = len(list(ontology.classes()))
    print("Total number of classes:", num_classes)

    num_individuals = len(list(ontology.individuals()))
    print("Total number of individuals:", num_individuals)

    classes_with_property = []
    for owl_class in ontology.classes():
        if owl_class.name not in ['Domain_entity', 'Independent_entity', 'Value']:
            for instance in owl_class.instances():
                for prop in instance.get_properties():
                    if property_name in prop.name:
                        classes_with_property.append(owl_class)
                        break
                    else:
                        continue

    print(f"Classes with the property '{property_name}':", classes_with_property)
    analyze_ontology(ontology)


if __name__ == "__main__":
    owl_name = "OWL_file1.owx"
    owl_file_path = owl_name
    check_ontology(owl_file_path, "start_date")
