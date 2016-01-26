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
     * Sets how many generations should pass before a status message should be displayed.
     * Setting {@code freq} to zero or a negative number will disable it.
     * @param freq the status message frequency
     */
    public final void setStatusFrequency(int freq) {
        this.freq = freq;
    }
    
    /**
     * Returns how many generations pass in between each status message.
     * A zero or negative value means this setting is disabled.
     * @return the status message frequency
     */
    public final int getStatusFrequency() {
        return freq;
    }
    
    /**
     * The status message to be printed while running the genetic algorithm.
     * This method can be overridden.
     */
    public void printStatusMessage() {
        System.out.printf("Generation: %d - best score: %s (%s).\n", generation, getBestIndividual().getFitness(), getBestIndividual());
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
     * Returns the mutation rate used by the default implementation
     * of {@code repopulate()}.
     * @see GeneticAlgorithm#repopulate()
     * @return the current mutation rate
     */
    public final double getMutationRate() {
        return mutationRate;
    }
    
    /**
     * Sets the mutation rate used by the default implementation
     * of {@code repopulate()} with the new value.
     * @see GeneticAlgorithm#repopulate()
     * @param rate the new mutation rate
     */
    public final void setMutatationRate(double rate) {
        mutationRate = rate;
    }
    
    /**
     * Repopulates the individuals in this genetic algorithm.
     * The default implementation divides the population in four parts and
     * uses multi-threading to created the new generation.
     * This method can be overridden.
     */
    @SuppressWarnings("unchecked")
    protected void repopulate() {
        for(int i = 0; i < population.length; i++) {
            population[i] = selector.select().crossover(selector.select());
            scores[i] = population[i].getFitness();

            if(Math.random() < mutationRate)
                population[i] = population[i].mutate();
        }
    }
    
    /**
     * Returns a copy of the internally stored {@code population} field, which
     * contains a {@code Chromosome} array.
     * @return {@code Chromosome[]}
     */
    public final C[] getPopulation() {
        return population.clone();
    }
    
    /**
     * Gets the individual located at the given {@code index}.
     * @param index the location of the desired individual {@code Chromosome}.
     * @return the specified individual
     */
    public final C getIndividual(int index) {
        return population[index];
    }
    
    /**
     * Returns the fitness score of the individual located at {@code index}.
     * Depending on the implementation, this may be more efficient
     * than {@code getIndividual(index).getFitness()}.
     * @param index the location of the desired individual {@code Chromosome}.
     * @return the specified fitness score
     */
    public final float getFitnessScore(int index) {
        return scores[index];
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
     * Returns the population size used by this {@code GeneticAlgorithm}.
     * @return population size
     */
    public final int getPopulationSize() {
        return population.length;
    }
    
    /**
     * Returns what generation number the {@code GeneticAlgorithm} is
     * currently on.
     * @return generation number
     */
    public final int getGeneration() {
        return generation;
    }
    
    /**
     * Runs the genetic algorithm until a solution is found.
     */
    @Override
    public final void run() {
        best = execute();
    }
    
    /**
     * Runs the genetic algorithm until a solution is found.
     * @return the solution {@code Chromosome}
     */
    public final C runToCompletion() {
        best = execute();
        return best;
    }
    
    /**
     * The abstract method that runs the genetic algorithm until
     * a solution is found. This method is not intended to be
     * executed by the result.
     * @return the solution {@code Chromosome}
     */
    protected abstract C execute();
    
    /**
     * {@inheritDoc}
     * @param other the object to be compared to {@code this} object
     */
    @Override
    public boolean equals(Object other) {
        if(other == null || this.getClass() != other.getClass())
            return false;
        
        return this.hashCode() == other.hashCode();
    }

    /**
     * {@inheritDoc} 
     */
    @Override
    public int hashCode() {
        int hash = 3;
        hash = 51 * hash + Arrays.hashCode(population);
        hash = 51 * hash + Arrays.hashCode(scores);
        hash = 51 * hash + selector.hashCode();
        hash = 51 * hash + best.hashCode();
        hash = 51 * hash + (int)(Double.doubleToLongBits(mutationRate) ^ (Double.doubleToLongBits(mutationRate) >>> 32));
        hash = 51 * hash + generation;
        hash = 51 * hash + freq;
        return hash;
    }
    
    /**
     * {@inheritDoc} 
     */
    @Override
    public void validateObject() throws InvalidObjectException {
        if(population == null)
            throw new InvalidObjectException("Population is null.");
        
        if(population.length == 0)
            throw new InvalidObjectException("Empty population.");
        
        if(generation < 0)
            throw new InvalidObjectException("Negative generation.");
    }
}
