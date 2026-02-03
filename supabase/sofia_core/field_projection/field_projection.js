/**
 * Field Projection - Action Projection
 * Part of the Field Action Triad for Sofia Core
 *
 * Projects the executed action into the environment.
 * Takes an action output, applies projection logic, and produces
 * an externalized effect. This is the field's outward expression layer.
 */
/**
 * Project field action into environment
 * Applies projection logic and produces externalized effect
 *
 * @param action - Action output to project
 * @param projector - Function that transforms action into externalized payload
 * @returns Projection event with projected=true and payload
 */
export function projectFieldAction(action, projector) {
    const payload = projector(action);
    return {
        projected: true,
        payload,
    };
}
//# sourceMappingURL=field_projection.js.map