/**
 * Field Expansion - Panoramic Field Expansion
 * Part of the Field Horizon Triad for Sofia Core
 *
 * Expands the apex expression into a wide-angle field state.
 * Accepts apex expression values, applies expansion logic,
 * and produces an expanded field state.
 * Represents "the field opens beyond the peak".
 * This is the system's panoramic-opening layer.
 */
/**
 * Expand field state from apex expression
 * Applies expansion logic and produces expanded field state
 *
 * @param apex - Apex expression value to expand
 * @param expander - Function that expands apex into wide-angle field
 * @returns Expansion state with expanded=true and expanded value
 */
export function expandFieldState(apex, expander) {
    const value = expander(apex);
    return {
        expanded: true,
        value,
    };
}
//# sourceMappingURL=field_expansion.js.map