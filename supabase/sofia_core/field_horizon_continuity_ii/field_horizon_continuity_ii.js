/**
 * Field Horizon Continuity-II - Second-Order Horizon-Scale Continuity
 * Part of the Field Horizon-II Triad for Sofia Core
 *
 * Stabilizes horizon-II scale continuity across cycles.
 * Accepts horizon-mapped-II values, applies second-order continuity logic,
 * and produces a continuous horizon-II state.
 * Represents "the second-order horizon remains stable across cycles".
 * This is the system's second-order horizon continuity layer.
 */
/**
 * Continue horizon state from horizon-mapped-II
 * Applies second-order continuity logic and produces continuous horizon-II state
 *
 * @param horizonMappedII - Horizon-mapped-II value to stabilize
 * @param continuer - Function that stabilizes horizon-II continuity
 * @returns Horizon Continuity-II state with continuous=true and stabilized value
 */
export function continueHorizonStateII(horizonMappedII, continuer) {
    const value = continuer(horizonMappedII);
    return {
        continuous: true,
        value,
    };
}
//# sourceMappingURL=field_horizon_continuity_ii.js.map