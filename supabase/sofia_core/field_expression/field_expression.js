/**
 * Field Expression - Identity-Based Expression
 * Part of the Field Identity Triad for Sofia Core
 *
 * Expresses identity outward into behavior.
 * This is the system's "I act as myself" layer.
 */
/**
 * Express field identity into behavior
 *
 * @param identity - The identity to express
 * @param expressor - Function that transforms identity into expression
 * @returns ExpressionState containing expression status and output
 */
export function expressFieldIdentity(identity, expressor) {
    const output = expressor(identity);
    return {
        expressed: true,
        output,
    };
}
//# sourceMappingURL=field_expression.js.map