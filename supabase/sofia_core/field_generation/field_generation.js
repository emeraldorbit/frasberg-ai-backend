/**
 * Field Generation - Generative Field Creation
 * Part of the Field Genesis Triad for Sofia Core
 *
 * Generates new field structures from the origin-state.
 * Accepts origin states, applies generative logic,
 * and produces a generated field state.
 * Represents "the field begins a new cycle of formation".
 * This is the system's generative-creation layer.
 */
/**
 * Generate new field state from origin using generator logic
 * Applies generative logic and produces generated state
 *
 * @param origin - Origin state to generate new structures from
 * @param generator - Function that generates new field structures
 * @returns Generation state with generated=true and generated value
 */
export function generateFieldState(origin, generator) {
    const value = generator(origin);
    return {
        generated: true,
        value,
    };
}
//# sourceMappingURL=field_generation.js.map