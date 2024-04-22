# Author: Junting Yang
# Student Number: 24043287

def main(csvfile):
    """
    The main function stores statistical values and information for each country and category of organization.
    
    Parameters:
    csvfile: The filename of the file containing organizational information.

    Return:
    Return a dictionary that stores the t-test score of profits and the Minkowski distance between two variables of each country.
    Meanwhile, return a nested dictionary that stores some information for each category of organizations.    
    """
    
    # Create a dictionary for storing t-test score and Minkowski distance for each country
    country_statistics_data = {}
    
    # Create a nested dictionary for storing organization information
    organization_category_information = {}

    # Initialize a set to store organization IDs that have been processed.
    unique_organization_ids = set()

    # Lists to store variables.
    organizations_id = []
    organizations_country = []
    organizations_category = []
    number_of_employees = []
    median_salary = []
    profit_2020 = []
    profit_2021 = []

    # Check if the file has a .csv extension, and if not, add it.
    if not csvfile.endswith('.csv'):
        csvfile = csvfile + '.csv'
    
    # Open and read the file.
    with open(csvfile, 'r') as organizations_file:
        header = organizations_file.readline().strip().split(",")  # Read the header to determine column order
        header_mapping = {col.lower(): i for i, col in enumerate(header)}

        # Check if required columns are missing in the header and exit if any are missing
        required_columns = ["organisation id", "country", "category", "number of employees", "median salary", "profits in 2020(million)", "profits in 2021(million)"]
        missing_columns = [col for col in required_columns if col.lower() not in header_mapping]
        if missing_columns:
              return [{}, {}]
        # Extract and store values from various columns in the data.
        for row in organizations_file:
            rowlist = row.strip().split(",")

            # Determine column indices based on column titles
            organization_id = rowlist[header_mapping["organisation id"]]
            country = rowlist[header_mapping["country"]].lower()
            category = rowlist[header_mapping["category"]].lower()

            try:
                num_employees = int(rowlist[header_mapping["number of employees"]])
                med_salary = float(rowlist[header_mapping["median salary"]])
                prof_2020 = float(rowlist[header_mapping["profits in 2020(million)"]])
                prof_2021 = float(rowlist[header_mapping["profits in 2021(million)"]])

                # Check if the number of employees and median salary are zero or negative.
                if num_employees <= 0 or med_salary <= 0:
                    continue

                # Check if the organization ID already exists.
                if organization_id in unique_organization_ids:
                    continue

                unique_organization_ids.add(organization_id)

                # Store data in appropriate lists
                organizations_id.append(organization_id)
                organizations_country.append(country)
                organizations_category.append(category)
                number_of_employees.append(num_employees)
                median_salary.append(med_salary)
                profit_2020.append(prof_2020)
                profit_2021.append(prof_2021)
            except ValueError:
                continue

    # Invoke the respective functions.
    country_t_test(organizations_country, profit_2020, profit_2021, country_statistics_data )
    country_m_distance(organizations_country, number_of_employees, median_salary, country_statistics_data )
    category_information(organizations_category, organizations_id, number_of_employees, profit_2020, profit_2021, organization_category_information)
    
    return country_statistics_data, organization_category_information
                

def country_t_test(organizations_country, profit_2020, profit_2021, country_statistics_data):
    """
    Computes the t-test score of profits in 2020 and 2021 for each country.
    
    Parameters:
    organizations_country: List of organization countries.
    profit_2020: List of profits of different organizations in 2020.
    profit_2021: List of profits of different organizations in 2021.
    country_statistics_data: Dictionary to store the results.
    """
    each_country = set(organizations_country)
    
    for country in each_country:
        # Extract profits for the specific country
        country_profit_2020 = [p for p, c in zip(profit_2020, organizations_country) if c == country]
        country_profit_2021 = [p for p, c in zip(profit_2021, organizations_country) if c == country]
        
        # Calculate means and standard deviations
        country_mean_2020 = sum(country_profit_2020) / len(country_profit_2020)
        country_mean_2021 = sum(country_profit_2021) / len(country_profit_2021)
        country_std_dev_2020 = (sum([(i - country_mean_2020) ** 2 for i in country_profit_2020]) / (len(country_profit_2020) - 1)) ** 0.5
        country_std_dev_2021 = (sum([(i - country_mean_2021) ** 2 for i in country_profit_2021]) / (len(country_profit_2021) - 1)) ** 0.5

        # Calculate t-score
        part_1 = (country_std_dev_2020)**2 / len(country_profit_2020)
        part_2 = (country_std_dev_2021)**2 / len(country_profit_2021)
        standard_error = (part_1 + part_2) ** 0.5
        t_score = (country_mean_2020 - country_mean_2021) / standard_error
        t_score = round(t_score, 4)
        country_statistics_data[country] = [t_score, None]



                    
def country_m_distance(organizations_country, number_of_employees,median_salary,country_statistics_data):
    """
    Computes Minkowski distance between the number of employees and the median salary for each country.
    
    Parameters:
    organizations_country: List of organization countries.
    number_of_employees: List of number of employees in each organization.
    median_salary: List of median salary of different organizations.
    country_statistics_data: Dictionary to store the results.
    """
    
    p = 3

    each_country = set(organizations_country)

    for country in each_country:
        
        country_employees = [n for n, c in zip(number_of_employees, organizations_country) if c == country]
        country_salary = [s for s, c in zip(median_salary, organizations_country) if c == country]

        m_distance = 0.0
        for num, sal in zip(country_employees, country_salary):
            difference = abs(num - sal) ** p
            m_distance += difference

        m_distance = m_distance ** (1/p)
    
        m_distance = round(m_distance, 4)
        
        country_statistics_data[country][1] = m_distance
def category_information(organizations_category, organizations_id, number_of_employees, profit_2020, profit_2021, organization_category_information):
    """
    Calculates and stores data related to each organization category, such as the id of an organization,
    the percentage of profit change from 2020 to 2021, and the rank of the organization within each category,
    with respect to the number of employees.

    Parameters:
    organizations_category: A list of organization categories.
    organizations_id: A list of IDs of different organizations.
    number_of_employees: A list of the number of employees in each organization.
    profit_2020: A list of profits of different organizations in 2020.
    profit_2021: A list of profits of different organizations in 2021.
    organization_category_information: A nested dictionary to store the results.
    """
    each_category = set(organizations_category)
    for category in each_category:
        organizations_in_category = [each_id for each_id, org_category in zip(organizations_id, organizations_category) if org_category == category]

        organization_data = []
        for each_id in organizations_in_category:
            index = organizations_id.index(each_id)
            profit_change = abs(profit_2020[index] - profit_2021[index])
            percentage_change = (profit_change / profit_2020[index]) * 100
            round_percentage_change = round(percentage_change, 4)

            organization_data.append((each_id, number_of_employees[index], round_percentage_change))

        organization_data.sort(key=lambda x: (-x[1], -x[2]))
        rank = 1
        previous_employee_number = None
        previous_percentage_change = None
        for i in organization_data:
            org_id, employee_number, change_profit = i
            if employee_number != previous_employee_number or change_profit != previous_percentage_change:
                rank += 1
            data_add_rank = (org_id, employee_number, change_profit, rank)
            organization_data[organization_data.index(i)] = data_add_rank
            previous_employee_number = employee_number
            previous_percentage_change = change_profit

        category_information = {}
        for data in organization_data:
            id, employee_count, change_percentage, rank = data
            category_information[id] = (employee_count, change_percentage, rank)

        organization_category_information[category] = category_information


                    
