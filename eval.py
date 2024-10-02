from nepal_constitution_ai.evaluation.eval import run_eval

if __name__ == "__main__" :

    result = run_eval() 

    # Display results
    for k,v in result.items():
        print(f"{k} = {v}")