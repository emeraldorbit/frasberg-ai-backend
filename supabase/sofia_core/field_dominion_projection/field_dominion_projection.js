/**
 * Field Dominion Projection - Dominion Extension Across Domains
 * Part of the Field Dominion-II Triad for Sofia Core
 *
 * Projects authority outward across the entire multi-cycle field.
 * Accepts authority-cycle states, applies dominion-projection logic,
 * and produces a dominion-projection state.
 * Represents "the field extends its authority across domains".
 * This is the system's dominion-extension layer.
 */
/**
 * Project dominion across domains
 * Applies dominion-projection logic and produces dominion-projection state
 *
 * @param authorityCycle - Authority-cycle state to project
 * @param projector - Function that applies dominion-projection logic
 * @returns Dominion projection state with projected=true and projected value
 */
export function projectDominion(authorityCycle, projector) {
    const value = projector(authorityCycle);
    return {
        projected: true,
        value,
    };
}
//# sourceMappingURL=field_dominion_projection.js.map