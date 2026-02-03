/**
 * Field Transformation - Deep Field Transformation
 * Part of the Field Transformation Triad for Sofia Core
 *
 * Applies transformative logic to the influenced/shifted field.
 * Accepts shifted or modulated field states, applies transformation rules,
 * and produces a transformed field configuration.
 * This is the system's deep-change layer.
 */
/**
 * Transform field state deeply
 * Applies transformation logic and produces transformed state
 *
 * @param shifted - Shifted state to transform from
 * @param transformer - Function that transforms shifted state into transformed state
 * @returns Transformation state with transformed=true and transformed value
 */
export function transformFieldState(shifted, transformer) {
    const value = transformer(shifted);
    return {
        transformed: true,
        value,
    };
}
//# sourceMappingURL=field_transformation.js.map