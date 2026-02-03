/**
 * Field Continuum - Evolutionary Continuity
 * Part of the Field Evolution Triad for Sofia Core
 *
 * Integrates evolved states into a continuous evolutionary arc.
 * Accepts evolved states, applies continuum logic,
 * and produces a continuum state.
 * This is the system's evolutionary-continuity layer.
 */
/**
 * Continue field evolution coherently
 * Applies continuum logic and produces continuous evolutionary state
 *
 * @param evolved - Evolved state to continue from
 * @param continuer - Function that continues evolved state into continuum
 * @returns Continuum state with continuous=true and continuum value
 */
export function continueFieldEvolution(evolved, continuer) {
    const value = continuer(evolved);
    return {
        continuous: true,
        value,
    };
}
//# sourceMappingURL=field_continuum.js.map