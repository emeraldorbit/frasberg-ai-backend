/**
 * Field Genesis Continuum - Renewal Continuity
 * Part of the Field Genesis Triad for Sofia Core
 *
 * Integrates generated states into the ongoing continuum.
 * Accepts generated states, applies genesis-continuity logic,
 * and produces a genesis-continuum state.
 * Represents "the field renews itself within the larger continuum".
 * This is the system's renewal-continuity layer.
 */
/**
 * Continue genesis by integrating generated state into continuum
 * Applies genesis-continuity logic and produces continuum state
 *
 * @param generated - Generated state to integrate into continuum
 * @param continuer - Function that integrates into ongoing continuum
 * @returns Genesis continuum state with continuous=true and continuum value
 */
export function continueGenesis(generated, continuer) {
    const value = continuer(generated);
    return {
        continuous: true,
        value,
    };
}
//# sourceMappingURL=field_genesis_continuum.js.map