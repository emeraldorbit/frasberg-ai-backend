/**
 * Field Continuum Extension - Long-Arc Continuum Extension
 * Part of the Field Continuum-II Triad for Sofia Core
 *
 * Extends the stabilized cycle into the long-arc continuum.
 * Accepts cycle-stable states, applies extension logic,
 * and produces a continuum-extension state.
 * Represents "the field extends beyond the current cycle".
 * This is the system's long-arc extension layer.
 */
/**
 * Extend field continuum by projecting cycle-stable state into long arc
 * Applies extension logic and produces continuum-extension state
 *
 * @param cycleStable - Cycle-stable state to extend
 * @param extender - Function that applies long-arc extension logic
 * @returns Continuum extension state with extended=true and extended value
 */
export function extendFieldContinuum(cycleStable, extender) {
    const value = extender(cycleStable);
    return {
        extended: true,
        value,
    };
}
//# sourceMappingURL=field_continuum_extension.js.map