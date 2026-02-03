/**
 * Field Signature - Identity Signature Formation
 * Part of the Field Identity Triad for Sofia Core
 *
 * Defines the system's unique identity signature.
 * This is the system's "who I am" layer.
 */
/**
 * Compute field signature from coherent cores
 *
 * @param cores - Array of coherent field cores to sign
 * @param signer - Function that computes signature from cores
 * @param validator - Function that validates the computed signature
 * @returns IdentitySignature containing signature and validation status
 * @throws Error if no cores are provided
 */
export function computeFieldSignature(cores, signer, validator) {
    if (cores.length === 0) {
        throw new Error('No coherent cores provided for signature computation');
    }
    const signature = signer(cores);
    const valid = validator(signature);
    return { signature, valid };
}
//# sourceMappingURL=field_signature.js.map