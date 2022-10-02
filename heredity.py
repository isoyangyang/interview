import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):
        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    joint_prob = 1

    # loop over all people
    for person in people:

        mother = people[person]["mother"]
        father = people[person]["father"]
        genes = inheritance(person, one_gene, two_genes)
        mom_genes = inheritance(mother, one_gene, two_genes)
        dad_genes = inheritance(father, one_gene, two_genes)
        has_trait = trait(person, have_trait)

        if mother is None:
            joint_prob *= (PROBS["gene"][genes] * PROBS["trait"][genes][has_trait])
        else:
            joint_prob *= PROBS["trait"][genes][has_trait] * child(genes, mom_genes, dad_genes)

    return joint_prob


def child(genes, mom_genes, dad_genes):
    """
    returns the probability child has given number of genes given the number of genes parents have
    :param genes:
    :param mom_genes:
    :param dad_genes:
    :return:
    """
    if genes == 0:
        # what is the probability that neither parent passed the gene
        return 1 - mutation(mom_genes) * 1 - mutation(dad_genes)
    elif genes == 1:
        # either mom_gene/dad_no_gene or mom_no_gene/dad_gene
        return mutation(mom_genes) * (1 - mutation(dad_genes)) + (1 - mutation(mom_genes)) * mutation(dad_genes)
    else:
        # both mom and dad passed the gene
        return mutation(mom_genes) * mutation(dad_genes)


def mutation(parent_genes):
    """
    returns the probability of passing the gene to offspring given the number of genes the parents has
    """
    if parent_genes == 2:
        return 0.99
    elif parent_genes == 1:
        return 0.5
    else:
        return 0.01


def inheritance(person, one_gene, two_genes):
    """
    returns the number of genes a person has by checking to which set person belongs to
    """
    if person in one_gene:
        return 1
    elif person in two_genes:
        return 2
    else:
        return 0


def trait(person, have_trait):
    """
    checks if person in have_trait set and returns True or False accordingly
    """
    if person in have_trait:
        return True
    else:
        return False


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # loop over all people
    for person in probabilities:

        has_trait = trait(person, have_trait)
        genes = inheritance(person, one_gene, two_genes)

        probabilities[person]["trait"][has_trait] = p
        probabilities[person]["gene"][genes] = p

    return


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    # loop over all people
    for person in probabilities:

        # trait normalization
        trait_sum = probabilities[person]["trait"][True] + probabilities[person]["trait"][False]
        probabilities[person]["trait"][True] = probabilities[person]["trait"][True] / trait_sum
        probabilities[person]["trait"][False] = probabilities[person]["trait"][False] / trait_sum

        # Genes normalization
        genes_sum = probabilities[person]["gene"][1] + probabilities[person]["gene"][2] + probabilities[person]["gene"][0]
        probabilities[person]["gene"][1] = probabilities[person]["gene"][1] / genes_sum
        probabilities[person]["gene"][2] = probabilities[person]["gene"][2] / genes_sum
        probabilities[person]["gene"][0] = probabilities[person]["gene"][0] / genes_sum

    return


if __name__ == "__main__":
    main()
