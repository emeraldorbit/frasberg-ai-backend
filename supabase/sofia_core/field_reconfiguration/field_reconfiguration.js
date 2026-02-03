/**
 * Field Reconfiguration - Structural Field Reconfiguration
 * Part of the Field Transformation Triad for Sofia Core
 *
 * Reconfigures the transformed field into a new structural pattern.
 * Accepts transformed states, applies reconfiguration logic,
 * and produces a reconfigured field state.
 * This is the system's structural-patterning layer.
 */
/**
 * Reconfigure field state structurally
 * Applies reconfiguration logic and produces reconfigured state
 *
 * @param transformed - Transformed state to reconfigure from
 * @param reconfigurer - Function that reconfigures transformed state into reconfigured state
 * @returns Reconfiguration state with reconfigured=true and reconfigured value
 */
export function reconfigureFieldState(transformed, reconfigurer) {
    const value = reconfigurer(transformed);
    return {
        reconfigured: true,
        value,
    };
}
//# sourceMappingURL=field_reconfiguration.js.map