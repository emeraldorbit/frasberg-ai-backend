/**
 * Field Uplift - Higher-Order Field Elevation
 * Part of the Field Ascension Triad for Sofia Core
 *
 * Elevates the evolved field into a higher-order configuration.
 * Accepts evolved field states, applies uplift logic,
 * and produces an uplifted field state.
 * Represents "the field rises to a higher tier".
 * This is the system's vertical-elevation layer.
 */
/**
 * Uplift field state to a higher tier
 * Applies uplift logic and produces uplifted state
 *
 * @param evolved - Evolved state to uplift from
 * @param uplifter - Function that uplifts evolved state into higher-order state
 * @returns Uplift state with uplifted=true and uplifted value
 */
export function upliftFieldState(evolved, uplifter) {
    const value = uplifter(evolved);
    return {
        uplifted: true,
        value,
    };
}
//# sourceMappingURL=field_uplift.js.map