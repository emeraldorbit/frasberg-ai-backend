/**
 * Field Constancy - Identity Constancy Across Cycles
 * Part of the Field Identity Triad for Sofia Core
 *
 * Maintains identity constancy across cycles.
 * This is the system's "I remain myself" layer.
 */
/**
 * Maintain field constancy across cycles
 *
 * @param previous - Previous identity state (null if first cycle)
 * @param current - Current identity state
 * @param comparator - Function that compares previous and current identity
 * @returns ConstancyState containing constancy flag and current identity
 */
export function maintainFieldConstancy(previous, current, comparator) {
    const constant = comparator(previous, current);
    return {
        constant,
        identity: current,
    };
}
//# sourceMappingURL=field_constancy.js.map