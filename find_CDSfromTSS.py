def find_nearby_lines(file, names, result_file):
    with open(file, 'r') as f:
        lines = f.readlines()

    results = []
    for name in names:
        found = False
        for i, line in enumerate(lines):
            if name in line:
                fields = line.strip().split('\t')
                if i > 0:
                    previous_line = lines[i-1].strip().split('\t')
                    if previous_line[2] != 'CDS':
                        previous_line = None
                else:
                    previous_line = None
                if i < len(lines) - 1:
                    next_line = None
                    for j in range(i+1, len(lines)):
                        next_fields = lines[j].strip().split('\t')
                        if next_fields[2] == 'CDS':
                            next_line = next_fields
                            break
                else:
                    next_line = None
                results.append((previous_line, line.strip(), next_line))
                found = True
                break

        if not found:
            results.append((None, None, None))

    # Save results to a file
    with open(result_file, 'w') as f:
        for name, result in zip(names, results):
            previous_line, found_line, next_line = result
            f.write(f"{name}\n")
            if found_line:
                if previous_line:
                    f.write("\t".join(previous_line) + "\n")

                if next_line:
                    f.write("\t".join(next_line) + "\n")
            else:
                f.write(f"No line found with the name {name}\n")
            f.write("\n")

# Example usage
file = 'HH103_annotated_sorted.gtf'
names_file = 'arac.txt'
result_file = 'new_promoters/results_fimo4.txt'

with open(names_file, 'r') as f:
    names = [line.strip() for line in f.readlines()]

find_nearby_lines(file, names, result_file)
print("Results have been saved in the file 'results.txt'.")
