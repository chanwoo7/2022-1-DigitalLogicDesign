def __get_prime_implicants(self, groups=None):

    if groups == None:
        groups = self.__initial_group()

    if len(groups) == 1:
        return groups[0]

    else:
        unused = []
        comparisons = range(len(groups) - 1)
        new_groups = [[] for c in comparisons]

        for compare in comparisons:
            group1 = groups[compare]
            group2 = groups[compare + 1]

            for term1 in group1:
                for term2 in group2:

                    term3 = term1.combine(term2)

                    if term3 != None:
                        term1.use()
                        term2.use()
                        if term3 not in new_groups[compare]:
                            new_groups[compare].append(term3)

        for group in groups:
            for term in group:
                if not term.used() and term not in unused:
                    unused.append(term)

        for term in self.__get_prime_implicants(new_groups):
            if not term.used() and term not in unused:
                unused.append(term)

        return unused


def __solve(self):
    prime_implicants = self.__get_prime_implicants(self.__initial_group())

    essential_prime_implicants = []
    values_used = [False] * len(self._values)

    for i in range(len(self._values)):
        value = self._values[i]

        uses = 0
        last = None
        for minterm in prime_implicants:
            if value in minterm.get_values():
                uses += 1
                last = minterm
        if uses == 1 and last not in essential_prime_implicants:
            for v in last.get_values():
                values_used[self._values.index(v)] = True
            essential_prime_implicants.append(last)

    if values_used.count(False) == 0:
        return essential_prime_implicants

    prime_implicants = [prime_implicant for prime_implicant in prime_implicants if
                        prime_implicant not in essential_prime_implicants]

    if len(prime_implicants) == 1:
        return essential_prime_implicants + prime_implicants

    return essential_prime_implicants + self.__power_set([
        self._values[index]
        for index in range(len(self._values))
        if not values_used[index]
    ], prime_implicants)
