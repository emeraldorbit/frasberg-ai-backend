/**
 * Field Continuity - Cross-Cycle Continuity Maintenance
 * Part of the Field Continuity Triad for Sofia Core
 *
 * Maintains continuity across cycles by carrying forward the temporal thread.
 * This is the system's temporal thread — the part that remembers the line it's walking.
 */
/**
 * Maintain field continuity across cycles
 *
 * @param previous - Previous cycle state (null for first cycle)
 * @param current - Current cycle state
 * @returns ContinuityState containing both previous and current states
 */
export function maintainFieldContinuity(previous, current) {
    return {
        previous,
        current,
    };
}
//# sourceMappingURL=field_continuity.js.map