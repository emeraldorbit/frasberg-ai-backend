/**
 * Field Horizon Continuity - Stable Horizon Continuity
 * Part of the Field Horizon Triad for Sofia Core
 *
 * Integrates the horizon map into a continuous, stable horizon field.
 * Accepts horizon map states, applies continuity logic,
 * and produces a horizon-continuity state.
 * Represents "the field stabilizes across the entire horizon".
 * This is the system's horizon-continuity layer.
 */
/**
 * Continue horizon state from horizon map
 * Applies continuity logic and produces horizon-continuity state
 *
 * @param horizonMap - Horizon map state to stabilize
 * @param continuer - Function that integrates horizon map into continuous field
 * @returns Horizon continuity state with continuous=true and continuous value
 */
export function continueHorizonState(horizonMap, continuer) {
    const value = continuer(horizonMap);
    return {
        continuous: true,
        value,
    };
}
//# sourceMappingURL=field_horizon_continuity.js.map