class QuineMcCluskeyAlgorithm:
    def __init__(self, minterm):
        self.num_var = minterm[0]
        self.PIs_dic = dict()
        self.EPIs_dic = dict()
        self.covers = []

        self.minterms = []
        for i in range(2, len(minterm)):
            self.minterms.append(minterm[i])

        self.minterms_dic = dict()
        for i in range(len(self.minterms)):
            if str(bin(self.minterms[i])).count('1') in self.minterms_dic:
                self.minterms_dic[str(bin(self.minterms[i])).count('1')].append(self.minterms[i])
            else:
                self.minterms_dic[str(bin(self.minterms[i])).count('1')] = []
                self.minterms_dic[str(bin(self.minterms[i])).count('1')].append(self.minterms[i])

        self.minterms_binary_dic = dict()
        for value in self.minterms_dic.values():
            for term in value:
                self.minterms_binary_dic[term] = bin(term).lstrip('0b').zfill(self.num_var)

        self.PIs = self.findPI()
        self.EPIs = self.findEPI()

        print("Instance created successfully!")

    def __str__(self):
        return f"Num of variance: {self.num_var}\n" \
               f"Prime Implicants: {self.PIs}\n" \
               f"Essential Prime Implicants: {self.EPIs}"

    # Step 1: Find Prime Implicants
    def findPI(self):
        while len(self.minterms_dic) != 0:
            key = 0
            new_minterms_dic = dict()
            new_minterms_binary_dic = dict()
            uncombined_dic = dict()
            for k, v in self.minterms_binary_dic.items():
                uncombined_dic[v] = k

            while key <= max(self.minterms_dic.keys()):
                same_merged_list = []
                over_onecnt_list = []

                if key not in self.minterms_dic.keys():
                    key += 1
                    continue
                if key + 1 not in self.minterms_dic.keys():
                    key += 1
                    continue

                for i in self.minterms_dic[key]:
                    for j in self.minterms_dic[key + 1]:
                        onecnt = 0
                        for k in range(self.num_var):
                            if (self.minterms_binary_dic[i][k] == '-' and self.minterms_binary_dic[j][k] != '-') or \
                                    (self.minterms_binary_dic[i][k] != '-' and self.minterms_binary_dic[j][k] == '-'):
                                if (i, j) not in same_merged_list:
                                    same_merged_list.append((i, j))
                            if self.minterms_binary_dic[i][k] != self.minterms_binary_dic[j][k]:
                                onecnt += 1
                            if onecnt > 1:
                                if (i, j) not in over_onecnt_list:
                                    over_onecnt_list.append((i, j))

                for i in self.minterms_dic[key]:
                    for j in self.minterms_dic[key + 1]:
                        for k in range(self.num_var):
                            if (i, j) not in same_merged_list and (i, j) not in over_onecnt_list and \
                                    self.minterms_binary_dic[i][k] != self.minterms_binary_dic[j][k]:
                                combined_minterm = (i, j)
                                combined_binary = self.minterms_binary_dic[i][:k] + '-' + \
                                                  self.minterms_binary_dic[i][k + 1:]

                                if self.minterms_binary_dic[i] in uncombined_dic:
                                    del uncombined_dic[self.minterms_binary_dic[i]]
                                if self.minterms_binary_dic[j] in uncombined_dic:
                                    del uncombined_dic[self.minterms_binary_dic[j]]

                                if combined_binary not in new_minterms_binary_dic.values():
                                    if key in new_minterms_dic:
                                        new_minterms_dic[key].append(combined_minterm)
                                    else:
                                        new_minterms_dic[key] = []
                                        new_minterms_dic[key].append(combined_minterm)

                                    new_minterms_binary_dic[combined_minterm] = combined_binary
                key += 1

            self.PIs_dic.update(uncombined_dic)
            self.minterms_dic = new_minterms_dic
            self.minterms_binary_dic = new_minterms_binary_dic

        for k in self.PIs_dic.keys():
            self.PIs_dic[k] = eval('(' + str(self.PIs_dic[k]).replace('(', '').replace(')', '') + ')')

        PIs = list(self.PIs_dic.keys())

        for i in range(len(PIs)):
            PIs[i] = PIs[i].replace('-', '2')
        PIs.sort()
        for i in range(len(PIs)):
            PIs[i] = PIs[i].replace('2', '-')

        return PIs

    # Step 2: Find Essential Prime Implicants
    def findEPI(self):
        count_dic = dict()
        one_count = []

        for num_tuple in self.PIs_dic.values():
            for num in num_tuple:
                if num in count_dic:
                    count_dic[num] += 1
                else:
                    count_dic[num] = 1

        for k in count_dic.keys():
            if count_dic[k] == 1:
                one_count.append(k)

        for k, num_tuple in self.PIs_dic.items():
            for num in num_tuple:
                if num in one_count:
                    if k not in self.EPIs_dic:  # 삭제 가능
                        self.EPIs_dic[k] = num_tuple

        EPIs = list(self.EPIs_dic.keys())
        for i in range(len(EPIs)):
            EPIs[i] = EPIs[i].replace('-', '2')
        EPIs.sort()
        for i in range(len(EPIs)):
            EPIs[i] = EPIs[i].replace('2', '-')

        self.covers += EPIs
        return EPIs

    # Step 3: Minimum Cover
    def findMinimumCover(self):
        cover_dic = dict(self.EPIs_dic)  # list로 해도 될 거 같으면 바꾸기
        remained_dic = dict(self.PIs_dic)

        print(remained_dic)
        # 딕셔너리 내에 저장된 튜플을 리스트로 변경
        for k in remained_dic.keys():
            remained_dic[k] = list(remained_dic[k])

        # while(이전 결과랑 똑같지 않으면)

        for k in self.EPIs_dic.keys():
            if k in remained_dic:
                del remained_dic[k]

        for k, v in remained_dic.items():
            for num_list in self.EPIs_dic.values():
                for num in num_list:
                    if num in v and num in remained_dic[k]:
                        remained_dic[k].remove(num)


        new_remained_dic = dict()
        cnt = 0

        while new_remained_dic != remained_dic:
            # remained_dic = new_remained_dic
            if cnt == 0:
                new_remained_dic = self.rowDominance(self.columnDominance(remained_dic))
            else:
                new_remained_dic = self.rowDominance(self.columnDominance(self.removeSecondaryEPI(remained_dic)))
            print(new_remained_dic)


        print(new_remained_dic)

    def removeSecondaryEPI(self, remained_dic):
        new_remained_dic = dict(remained_dic)
        SecondaryEPIs_dic = dict()
        count_dic = dict()
        one_count = []

        for num_list in remained_dic.values():
            for num in num_list:
                if num in count_dic:
                    count_dic[num] += 1
                else:
                    count_dic[num] = 1

        for k in count_dic.keys():
            if count_dic[k] == 1:
                one_count.append(k)

        for k, num_list in remained_dic.items():
            for num in num_list:
                if num in one_count:
                    if k not in SecondaryEPIs_dic:
                        SecondaryEPIs_dic[k] = num_list

        for k in SecondaryEPIs_dic.keys():
            if k in new_remained_dic:
                del new_remained_dic[k]

        for k, v in new_remained_dic.items():
            for num_list in SecondaryEPIs_dic.values():
                for num in num_list:
                    if num in v and num in new_remained_dic[k]:
                        new_remained_dic[k].remove(num)

        self.covers += list(SecondaryEPIs_dic.keys())

        return new_remained_dic

    # Step 3-3: Apply Row Dominance Law
    def rowDominance(self, remained_dic):
        new_remained_dic = dict(remained_dic)

        biggest_bins_list = []
        for k1 in new_remained_dic.keys():
            biggest_bins = new_remained_dic[k1]
            for k2 in new_remained_dic.keys():
                if k1 != k2:
                    if new_remained_dic[k2] == biggest_bins:
                        continue
                    elif set(new_remained_dic[k2]) | set(biggest_bins) == set(new_remained_dic[k2]):
                        biggest_bins = new_remained_dic[k2]
            if biggest_bins != new_remained_dic[k1] and biggest_bins not in biggest_bins_list:
                biggest_bins_list.append(biggest_bins)

        need_to_remove = []
        interchangable = []

        for biggest_bins in biggest_bins_list:
            for k in new_remained_dic.keys():
                if new_remained_dic[k] == biggest_bins:
                    interchangable.append(k)
                elif set(new_remained_dic[k]) & set(biggest_bins) == set(new_remained_dic[k]) and k not in need_to_remove:
                    need_to_remove.append(k)
        for binary in need_to_remove:
            del new_remained_dic[binary]

        checked = []
        if len(interchangable) >= 2:
            for binary in interchangable:
                if new_remained_dic[binary] in checked:
                    del new_remained_dic[binary]
                else:
                    checked.append(new_remained_dic[binary])

        return new_remained_dic

    # Step 3-2: Apply Column Dominance Law
    def columnDominance(self, remained_dic):
        new_remained_dic = dict()
        columns_dic = dict()

        for k, num_list in remained_dic.items():
            for num in num_list:
                if num in columns_dic:
                    columns_dic[num].append(k)
                else:
                    columns_dic[num] = []
                    columns_dic[num].append(k)

        smallest_bins_list = []
        for k1 in columns_dic.keys():
            smallest_bins = columns_dic[k1]
            for k2 in columns_dic.keys():
                if k1 != k2:
                    if columns_dic[k2] == smallest_bins:
                        continue
                    elif set(columns_dic[k2]) & set(smallest_bins) == set(columns_dic[k2]):
                        smallest_bins = columns_dic[k2]
            if smallest_bins != columns_dic[k1] and smallest_bins not in smallest_bins_list:
                smallest_bins_list.append(smallest_bins)

        need_to_remove = []
        interchangable = []
        for smallest_bins in smallest_bins_list:
            for k in columns_dic.keys():
                if columns_dic[k] == smallest_bins:
                    interchangable.append(k)
                elif set(columns_dic[k]) | set(smallest_bins) == set(columns_dic[k]) and k not in need_to_remove:
                    need_to_remove.append(k)

        for num in need_to_remove:
            del columns_dic[num]

        checked = []
        if len(interchangable) >= 2:
            for num in interchangable:
                if columns_dic[num] in checked:
                    del columns_dic[num]
                else:
                    checked.append(columns_dic[num])

        for k, bin_list in columns_dic.items():
            for bin in bin_list:
                if bin in new_remained_dic:
                    new_remained_dic[bin].append(k)
                else:
                    new_remained_dic[bin] = []
                    new_remained_dic[bin].append(k)

        return new_remained_dic


# a = QuineMcCluskeyAlgorithm([4, 8, 0, 4, 8, 10, 11, 12, 13, 15])
# a = QuineMcCluskeyAlgorithm([4, 16, 0, 1, 2, 4, 5, 6, 8, 9, 10, 11, 12, 14, 15])
# a = QuineMcCluskeyAlgorithm([4, 16, 0, 1, 2, 4, 5, 6, 8, 9, 10, 11, 12, 14, 15])
print(a)
a.findMinimumCover()
# print(a.removeSecondaryEPI({'a': [10], 'b': [10, 11], 'c': [13], 'd': [11, 15], 'e': [13, 15], 'f': [12]}))
# print(a.columnDominance({'10-0': [10], '101-': [10, 11], '110-': [13], '1-11': [11, 15], '11-1': [13, 15]}))
# print()
# print(a.rowDominance({'10-0': [10], '101-': [10, 11], '110-': [13], '1-11': [11, 15], '11-1': [13, 15]}))
# print(a.PIs_dic)
# print(a.EPIs_dic)
# print([x for x in a.PIs if x not in a.EPIs])