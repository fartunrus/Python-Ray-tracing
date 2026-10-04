class vacancy:
    def __init__(self, company, salary, exp):
        self.company = company
        self.salary = salary
        self.exp = exp
class Job:
    vacancies = []
    def __init__(self, name):
        self.name = name
    def find_by_company(self, company):
        for i in range(len(self.vacancies)):
            if(self.vacancies[i].company == company):
                return i
    def post_vacancy(self, company, salary, min_exp):
        self.vacancies.append(vacancy('"'+company+'"', salary, min_exp))
    def close_vacancy(self, company):
        del self.vacancies[find_by_company(company)]
    def update_salary(self, company, new_salary):
        self.vacancies[find_by_company(company)].salary = new_salary
    def update_exp(self, company, new_exp):
        self.vacancies[find_by_company(company)].exp = new_exp
    def show_vacancies(self):
        print(self.name)
        if(len(self.vacancies)>0):
            for i in range(len(self.vacancies)):
                print(self.vacancies[i].company + ": зарплата " + str(self.vacancies[i].salary) + " тыс, требуемый опыт " + str(self.vacancies[i].exp))
        else:
            print("Пока нет вакансий на данную профессию")
    def find_best_vacancy(self, exp, proffesion, min_salary):
        if(self.name == '"'+proffesion+'"'):
            if(len(self.vacancies)>0):
                salary=0
                a=-1
                for i in range(len(self.vacancies)):
                    if(self.vacancies[i].exp<=exp and self.vacancies[i].salary>min_salary):
                        salary = self.vacancies[i].salary
                        a = i
                if(a>=0):
                    print("Наилучшаяя вакансия для вас в компании " + vacancies[a].company + " с зарплатой " + str(salary) + " тыс.")
                else:
                    print("Пока нет вакансий на данную профессию")
        else:
            print("Кажется, вы ищете вакансии в разделе " + name + ". Выберите другой раздел.")
loyer = Job('loyer')
loyer.show_vacancies()
loyer.post_vacancy('Хорошие юристы', 300, 15)
loyer.show_vacancies()