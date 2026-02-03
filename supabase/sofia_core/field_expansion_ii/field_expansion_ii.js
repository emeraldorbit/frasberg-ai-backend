/**
 * Field Expansion-II - Second-Order Panoramic Field Expansion
 * Part of the Field Horizon-II Triad for Sofia Core
 *
 * Expands the apex-II expression into a second-order wide-angle field state.
 * Accepts apex-II expression values, applies second-order expansion logic,
 * and produces an expanded field-II state.
 * Represents "the field opens beyond the second-order peak".
 * This is the system's second-order panoramic-opening layer.
 */
/**
 * Expand field state from apex-II expression
 * Applies second-order expansion logic and produces expanded field-II state
 *
 * @param apexII - Apex-II expression value to expand
 * @param expander - Function that expands apex-II into wide-angle field
 * @returns Expansion-II state with expanded=true and expanded value
 */
export function expandFieldStateII(apexII, expander) {
    const value = expander(apexII);
    return {
        expanded: true,
        value,
    };
}
//# sourceMappingURL=field_expansion_ii.js.map