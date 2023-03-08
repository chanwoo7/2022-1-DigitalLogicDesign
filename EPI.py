def findPI(minterm):
    num_var = minterm[0]
    finally_uncombined_dic = dict()

    minterms = []
    for i in range(2, len(minterm)):
        minterms.append(minterm[i])

    minterms_dic = dict()
    for i in range(len(minterms)):
        if str(bin(minterms[i])).count('1') in minterms_dic:
            minterms_dic[str(bin(minterms[i])).count('1')].append(minterms[i])
        else:
            minterms_dic[str(bin(minterms[i])).count('1')] = []
            minterms_dic[str(bin(minterms[i])).count('1')].append(minterms[i])

    minterms_binary_dic = dict()
    for value in minterms_dic.values():
        for term in value:
            minterms_binary_dic[term] = bin(term).lstrip('0b').zfill(num_var)

    while len(minterms_dic) != 0:
        key = 0
        new_minterms_dic = dict()
        new_minterms_binary_dic = dict()
        uncombined_dic = dict()
        for k, v in minterms_binary_dic.items():
            uncombined_dic[v] = k

        while key <= max(minterms_dic.keys()):
            same_merged_list = []
            over_onecnt_list = []

            if key not in minterms_dic.keys():
                key += 1
                continue
            if key + 1 not in minterms_dic.keys():
                key += 1
                continue

            for i in minterms_dic[key]:
                for j in minterms_dic[key + 1]:
                    onecnt = 0
                    for k in range(num_var):
                        if (minterms_binary_dic[i][k] == '-' and minterms_binary_dic[j][k] != '-') or \
                                (minterms_binary_dic[i][k] != '-' and minterms_binary_dic[j][k] == '-'):
                            if (i, j) not in same_merged_list:
                                same_merged_list.append((i, j))
                        if minterms_binary_dic[i][k] != minterms_binary_dic[j][k]:
                            onecnt += 1
                        if onecnt > 1:
                            if (i, j) not in over_onecnt_list:
                                over_onecnt_list.append((i, j))

            for i in minterms_dic[key]:
                for j in minterms_dic[key + 1]:
                    for k in range(num_var):
                        if (i, j) not in same_merged_list and (i, j) not in over_onecnt_list and \
                                minterms_binary_dic[i][k] != minterms_binary_dic[j][k]:
                            combined_minterm = (i, j)
                            combined_binary = minterms_binary_dic[i][:k] + '-' + minterms_binary_dic[i][k + 1:]

                            if minterms_binary_dic[i] in uncombined_dic:
                                del uncombined_dic[minterms_binary_dic[i]]
                            if minterms_binary_dic[j] in uncombined_dic:
                                del uncombined_dic[minterms_binary_dic[j]]

                            if combined_binary not in new_minterms_binary_dic.values():
                                if key in new_minterms_dic:
                                    new_minterms_dic[key].append(combined_minterm)
                                else:
                                    new_minterms_dic[key] = []
                                    new_minterms_dic[key].append(combined_minterm)

                                new_minterms_binary_dic[combined_minterm] = combined_binary
            key += 1

        finally_uncombined_dic.update(uncombined_dic)
        minterms_dic = new_minterms_dic
        minterms_binary_dic = new_minterms_binary_dic

    for k in finally_uncombined_dic.keys():
        finally_uncombined_dic[k] = eval('(' + str(finally_uncombined_dic[k]).replace('(', '').replace(')', '') + ')')

    return finally_uncombined_dic


def solution(minterm):
    finally_uncombined_dic = findPI(minterm)
    count_dic = dict()
    one_count = []
    PIs = list(finally_uncombined_dic.keys())
    EPIs = []

    for num_tuple in finally_uncombined_dic.values():
        for num in num_tuple:
            if num in count_dic:
                count_dic[num] += 1
            else:
                count_dic[num] = 1

    for k in count_dic.keys():
        if count_dic[k] == 1:
            one_count.append(k)

    for k, num_tuple in finally_uncombined_dic.items():
        for num in num_tuple:
            if num in one_count:
                if k not in EPIs:
                    EPIs.append(k)

    for i in range(len(PIs)):
        PIs[i] = PIs[i].replace('-', '2')
    PIs.sort()
    for i in range(len(PIs)):
        PIs[i] = PIs[i].replace('2', '-')

    for i in range(len(EPIs)):
        EPIs[i] = EPIs[i].replace('-', '2')
    EPIs.sort()
    for i in range(len(EPIs)):
        EPIs[i] = EPIs[i].replace('2', '-')

    print(count_dic)
    print(one_count)
    print(EPIs)

    answer = PIs + ['EPI'] + EPIs
    return answer


print(solution([4, 8, 0, 4, 8, 10, 11, 12, 13, 15]))
# print(solution([3, 6, 0, 1, 2, 5, 6, 7]))
# print(solution([3, 4, 3, 5, 6, 7]))
# print(solution([6, 64, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63]))
