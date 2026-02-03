/**
 * Field Reintegration - Global Field Reintegration
 * Part of the Field Transformation Triad for Sofia Core
 *
 * Reintegrates the reconfigured field back into the global field.
 * Accepts reconfigured states, applies reintegration logic,
 * and produces a reintegrated, globally coherent field state.
 * This is the system's ability to transform without fragmentation.
 */
/**
 * Reintegrate field state into global coherence
 * Applies reintegration logic and produces reintegrated state
 *
 * @param reconfigured - Reconfigured state to reintegrate from
 * @param reintegrator - Function that reintegrates reconfigured state into global field
 * @returns Reintegration state with reintegrated=true and reintegrated value
 */
export function reintegrateFieldState(reconfigured, reintegrator) {
    const value = reintegrator(reconfigured);
    return {
        reintegrated: true,
        value,
    };
}
//# sourceMappingURL=field_reintegration.js.map