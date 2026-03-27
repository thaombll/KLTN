

def pipeline_storytelling(database_name, intention):
    connection_database()
    information_database = understanding_data(database_name)
    list_question = generation_question(information_database)
    data_mining_dataset = query_database(list_question)
    storytelling = baseline_storytelling(data_mining_dataset, intention)
    return storytelling

if __name__ == "__main__":
    database_name = 
    question_user = 
    storytelling = pipeline_storytelling(database_name, question_user)
    print(storytelling)