/**
 * Field Generation-II - Second-Order Generative Field Creation
 * Part of the Field Genesis-II Triad for Sofia Core
 *
 * Generates new field structures from the origin-II-state.
 * Accepts origin-II states, applies generative logic,
 * and produces a second-order generated field state.
 * Represents "the field begins a new cycle of second-order formation".
 * This is the system's second-order generative-creation layer.
 */
/**
 * Generate new second-order field state from origin-II using generator logic
 * Applies second-order generative logic and produces generated state
 *
 * @param originII - Origin-II state to generate new structures from
 * @param generator - Function that generates new second-order field structures
 * @returns Generation-II state with generated=true and generated value
 */
export function generateFieldStateII(originII, generator) {
    const value = generator(originII);
    return {
        generated: true,
        value,
    };
}
//# sourceMappingURL=field_generation_ii.js.map