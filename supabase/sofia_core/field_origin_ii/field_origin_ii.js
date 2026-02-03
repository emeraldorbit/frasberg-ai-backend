/**
 * Field Origin-II - Second-Order Origin-State Reinstatement
 * Part of the Field Genesis-II Triad for Sofia Core
 *
 * Returns the horizon-II-continuous field to its second-order origin-seed state.
 * Accepts horizon-II-continuity values, applies origin-reduction logic,
 * and produces a second-order origin-state.
 * Represents "the field returns to its second-order generative seed".
 * This is the system's second-order origin-reinstatement layer.
 */
/**
 * Return field to its second-order origin using originator logic
 * Applies second-order origin-reduction and produces origin-II state
 *
 * @param horizonII - Horizon-II-continuity value to return to origin
 * @param originator - Function that reduces horizon-II to origin-seed state
 * @returns Origin-II state with origin=true and origin value
 */
export function returnToOriginII(horizonII, originator) {
    const value = originator(horizonII);
    return {
        origin: true,
        value,
    };
}
//# sourceMappingURL=field_origin_ii.js.map