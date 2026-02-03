/**
 * Field Dominion Continuity - Persistent Dominion Stability
 * Part of the Field Dominion-II Triad for Sofia Core
 *
 * Stabilizes dominion across cycles, ensuring persistent structural governance.
 * Accepts dominion-projection states, applies dominion-continuity logic,
 * and produces a dominion-continuity state.
 * Represents "the field maintains sovereign continuity across cycles".
 * This is the system's dominion-stability layer.
 */
/**
 * Continue dominion across cycles
 * Applies dominion-continuity logic and produces dominion-continuity state
 *
 * @param dominionProjection - Dominion-projection state to continue
 * @param continuer - Function that applies dominion-continuity logic
 * @returns Dominion continuity state with continuous=true and continuous value
 */
export function continueDominion(dominionProjection, continuer) {
    const value = continuer(dominionProjection);
    return {
        continuous: true,
        value,
    };
}
//# sourceMappingURL=field_dominion_continuity.js.map