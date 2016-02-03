package aisutil.genetic;

import java.io.InvalidObjectException;
import java.io.ObjectInputValidation;

import java.util.Arrays;

/**
 * Creates an object that can be used to
 * manipulate the current state of the
 * genetic algorithm being used to
 * seek the solution to a problem.
 * @param <C> the type of {@code Chromosome} to be dealt with
 * @see aisutil.genetic.MaxGenerationGeneticAlgorithm
 * @see aisutil.genetic.PerfectGeneticAlgorithm
 * @see aisutil.genetic.ThresholdGeneticAlgorithm
 * @author ammon smith
 */
public abstract class GeneticAlgorithm<C extends Chromosome<C>> implements Runnable, ObjectInputValidation {
    protected final C[] population;
    protected final float[] scores;
    protected final Selector<C> selector;
    private C best;
    private double mutationRate = 0.05;
    private int generation;
    private int freq;
    
    /**
     * Creates a {@code GeneticAlgorithm} object used to 
     * @param populationSize the population size of each generation
     * @param selector the {@code Selector} used to create a new
     * population of individuals
     * @param seeder the {@code PopulationSeeder} that is used to
     * create the first generation of individuals
     */
    @SuppressWarnings({"LeakingThisInConstructor", "unchecked"})
    public GeneticAlgorithm(int populationSize, Selector<C> selector, PopulationSeeder<C> seeder) {
        if(populationSize <= 0)
            throw new IllegalArgumentException("Invalid population size: " + populationSize);
        
        this.selector = selector;
        this.population = (C[])new Chromosome<?>[populationSize];
        this.scores = new float[populationSize];
        
        for(int i = 0; i < populationSize; i++)
            scores[i] = Float.NaN;
        
        selector.setGeneticAlgorithm(this);
        initPopulation(seeder);
        initFitness();
    }
    
    @SuppressWarnings("LeakingThisInConstructor")
    public GeneticAlgorithm(C[] population, Selector<C> selector) {
        this.selector = selector;
        this.population = population.clone();
        this.scores = new float[population.length];
        
        selector.setGeneticAlgorithm(this);
        initFitness();
    }
    
    /**
     * A constructor for {@code Selector}s to make a {@code GeneticAlgorithm}
     * exclusively for population management.
     * @param population the population of individuals
     */
    GeneticAlgorithm(C[] population) {
        this.selector = null;
        this.scores = null;
        this.population = population;
    }
    
    private void initPopulation(final PopulationSeeder<C> seeder) {
        for(int i = 0; i < scores.length; i++)
            population[i] = seeder.newIndividual();
    }
    
    private void initFitness() {
        for(int i = 0; i < scores.length; i++)
            scores[i] = population[i].getFitness();
    }

    /**
     * Initializes the next generation of the genetic algorithm.
     */
    public final void nextGeneration() {
        for(int i = 0; i < scores.length; i++)
            scores[i] = population[i].getFitness();
        
        if(freq > 0 && (generation % freq == 0 || generation == 0))
            printStatusMessage();
        
        repopulate();
        generation++;
    }

    /**
     * Finds and returns the {@code Chromosome} with the best
     * fitness score. If multiple {@code Chromosome}s are found
     * with the same high score, the first one is returned.
     * @return the best {@code Chromosome} in this generation
     */
    public final C getBestIndividual() {
        if(best != null)
            return best;
        
        int id = 0;
        float score = scores[0];
        
        if(selector.hasNaturalOrdering) {
            for(int i = 1; i < population.length; i++) {
                if(scores[i] > score) {
                    id = i;
                    score = scores[i];
                }
            }
        } else {
            for(int i = 1; i < population.length; i++) {
                if(scores[i] < score) {
                    id = i;
                    score = scores[i];
                }
            }
        }
        
        return population[id];
    }
    
    /**
     * The abstract method that runs the genetic algorithm until
     * a solution is found. This method is not intended to be
     * executed by the result.
     * @return the solution {@code Chromosome}
     */
    protected abstract C execute();
}

