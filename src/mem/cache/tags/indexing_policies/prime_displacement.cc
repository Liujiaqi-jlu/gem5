/**
 * @file
 * Definitions of a prime modulo indexing policy.
 */

#include "mem/cache/tags/indexing_policies/prime_displacement.hh"

#include "base/bitfield.hh"
#include "base/intmath.hh"
#include "base/logging.hh"
#include "mem/cache/replacement_policies/replaceable_entry.hh"

PrimeDisplacement::PrimeDisplacement(const Params *p)
    : BaseIndexingPolicy(p),
      modulo(p->modulo)
{
    fatal_if(!isPrime(modulo), "modulo should be a prime");
    fatal_if(!(modulo < numSets), "modulo should be a prime less than the \
        number of sets");
}

bool PrimeDisplacement::isPrime(const uint64_t modulo) const {
    if (modulo <= 1)
        return false;
    if (modulo == 2)
        return true;
    for (unsigned int i = 2; i <= sqrt(modulo); ++i)
        if (modulo % i == 0)
            return false;
    return true;
}

uint32_t
PrimeDisplacement::extractSet(const Addr addr) const
{
    uint32_t originalIndex = (addr >> setShift) & setMask;

    return (modulo*extractTag(addr) + originalIndex) % numSets;
}

Addr
PrimeDisplacement::regenerateAddr(const Addr tag,
    const ReplaceableEntry* entry) const
{
    size_t offset = tag*modulo;
    int64_t originalIndex = -1;
    for (size_t i = 0; i < numSets; i++) {
        if ((offset + i) % numSets == entry->getSet()) {
            originalIndex = i;
            break;
        }
    }

    fatal_if(originalIndex == -1, "Atmn is still an idiot");

    return (tag << tagShift) | (originalIndex << setShift);
}

std::vector<ReplaceableEntry*>
PrimeDisplacement::getPossibleEntries(const Addr addr) const
{
    return sets[extractSet(addr)];
}

PrimeDisplacement*
PrimeDisplacementParams::create()
{
    return new PrimeDisplacement(this);
}
