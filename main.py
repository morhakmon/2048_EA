from Agent import Agent
import copy
import wandb


if __name__ == '__main__':

    wandb.init(
        # set the wandb project where this run will be logged
        project="2048 Evolution Algorithm ",

        # track hyperparameters and run metadata
        config={
            "number of generations": 200,
            "generation size": 640,
            "mutation level": 0.3,
            "cross-over level": 0.5,
            "mutation description-": "unchanged",
            "crossover description-": "unchanged",
            "score methode-": "non - but more power to the tile"
        }
    )

    generation_size = 640
    generation = [Agent() for _ in range(generation_size)]  # create the first generation
    num_of_generation = 200
    for generation_idx in range(num_of_generation):  # for each generation
        for idx, chromosome in enumerate(generation):  # for each individual in generation
            chromosome.fitness()  # update the fitness and game score
        generation = sorted(generation, key=lambda x: x.fitness_score, reverse=True)  # sort from the best to the worst

        print("Best score of generation {} is {}".format(generation_idx, generation[0].game_score))
        # send to wandb
        wandb.log({"Fitness Score": generation[0].fitness_score, "Game Score": generation[0].game_score})

        # Create the new generation
        # best 5 keep unchanged
        # multiply the first 5, 5 time each and apply mutation
        for idx in range(40, 240):
            child = generation[int(idx/40) - 1]
            generation[idx] = copy.deepcopy(child)
            generation[idx].mutate(0.3)

        # do cross over in the best 10
        for idx in range(240, 320):
            child = generation[idx - 240]
            generation[idx] = copy.deepcopy(child)
            parent_chrome_b = generation[idx - 239]
            generation[idx].crossover(parent_chrome_b, 0.5)

        # add some completely new blood
        for idx in range(320, 640):
            generation[idx] = Agent()

    wandb.finish()



