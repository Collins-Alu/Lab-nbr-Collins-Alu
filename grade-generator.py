import csv
from dataclasses import dataclass
from typing import List

@dataclass 
class Assignment:
    name: str
    category: str # 'FA' or 'SA'
    grade:float 
    weight: float

def input_nonempty(prompt: str) -> str:
    while True:
        v =  input(prompt) .strip()
        if v:
            return v
        print("Can't be blank. Try again.")

def input_category(prompt: str) -> str:
    while True:
        v = input(prompt) .strip() .upper()
        if v in ("FA", "SA"):
            return v
        print ("Category must be 'FA' or 'SA'.")

def input_float_in_range(prompt: str, min_val: float = None, max_val: float = None) -> float:
    while True:
        s = input(prompt). strip()
        try:
            v = float(s)
        except ValueError:
            print("Enter a valid number")
            continue
        if (min_val is not None and v < min_val) or (max_val is not None and v > max_val):
            rng = []
            if min_val is not None:
                rng.append(f">= {min_val}")
            if max_val is not None:
                rng.append(f"<= {max_val}")
            print(f"Enter a value{' and' .join(rng)}.")
            continue
        return v
 
def input_assignment() -> Assignment:
    name = input_nonempty("Assignment name: ")
    category = input_category("category (FA/SA): ") 
    grade = input_float_in_range("Grade obtained (0-100): ", 0.0, 100.0)
    weight = input_float_in_range("Weight (positive number): ", 0.0000001, None)
    return Assignment(name = name, category=category, grade=grade, weight=weight)


def calculate(assignments: List[Assignment]):
    t_FA = 0.0
    t_SA = 0.0
    for a in assignments:
       weighted = (a.grade / 100.0) *a.weight
       if a.category =='FA':
            t_FA += weighted
       else:
           t_SA += weighted  

    sum_fa_weights = sum(a.weight for a in assignments if a.category == 'FA') 
    sum_sa_weights = sum(a.weight for a in assignments if a.category == 'SA')

    t_grade = t_FA + t_SA

    gpa = (t_grade / 100.0) * 5.0

    pass_fa = ( t_FA >= 0.5 * sum_fa_weights) if sum_fa_weights == 0 else True
    pass_sa = ( t_SA >= 0.5 * sum_sa_weights) if sum_sa_weights == 0 else True
    passed = pass_fa + pass_sa 
    return {
    't_FA': t_FA,
    't_SA': t_SA,
    't_grade': t_grade,
     'gpa': gpa,
    'passed': passed,
    'sum_fa_weights': sum_fa_weights,
    'sum_sa_weights': sum_sa_weights
    }


def save_csv(assignments, filename='grades_csv'):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer (f)
        writer.writerow(['Assignment', 'Category', 'Grade', 'Weight'])
        for a in assignments:
            writer.writerow([a.name, a.category, a.grade, a.weight])


def print_summary(results):
    print(f"Formative points: {results['FA']: .2f} {results['sum_fa_weights']: .2f} ")
    print(f"Summative points: {results['SA']: .2f} {results['sum_sa_weights']: .2f} ")
    print(f"Final Total: {results['total_grade']:.2f} / {(results['sum_fa_weights']+results['sum_sa_weights']):.2f}")
    print(f"GPA (scale 5): {results['gpa']:.2f}")
    status = "PASSED" if results['passed'] else" FAILED"
    print(f"Status: {status}")

def main():
    print("Grade Generator - enter assignments.")
    assignments: list[Assignment] = []
    while True:
        assignments.append (input_assignment)
        cont = input ("Add assignment? (y/n): "). strip(). lower() 
        if cont == 'n':
            break

    if not assignments:
        print("No assignments entered. Exiting.")
        return
    
    results = calculate(Assignment)
    print_summary(results)
    save_csv(assignments)
    print ("Saved assignments to grades.csv")

if __name__ == '__main__':
    main()

        

         



