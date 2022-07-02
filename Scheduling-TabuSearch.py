#!/usr/bin/env python
# coding: utf-8

# In[46]:



import copy
import argparse
import operator
import time
import random
import pandas as pd
from tabulate import tabulate



# In[20]:

def calcComp(set_up_merging, proc_time, Demand, mach_to_jobs):

    num_mach = 5  # number of machines
    num_jobs =92  # number of jobs
    job_comp_times = [0] * num_jobs
    machine_comp_times = [0] * num_mach # set all completion time of the machines zero

    for k in range(0, (num_mach)):
        if len(mach_to_jobs[k]) != 0:
            first_job = mach_to_jobs[k][0]
            job_comp_times[first_job] = proc_time[first_job][k]* Demand[0][first_job]
            machine_comp_times[k] = float(job_comp_times[first_job])
            #Calculate  job and machine completion time of first job

    for i in range(0,len(mach_to_jobs)):
        if len(mach_to_jobs[i]) == 0:
            continue

        for j in range(1, len(mach_to_jobs[i])):
            job = mach_to_jobs[i][j]
            prev_job = mach_to_jobs[i][j - 1]

            job_comp_times[job] = machine_comp_times[i]+set_up_merging[i][prev_job][job]+ proc_time[job][i] * Demand[0][job]
            machine_comp_times[i] = float(job_comp_times[job])
            # Calculate  job and machine completion time of other than first jobs


    return machine_comp_times,job_comp_times

def generate_first_solution(set_up_merging, proc_time, Demand, random_first_sol):

    num_mach = 5
    num_jobs = 92
    jobs_to_machines = [0] * num_jobs
    job_comp_times = [0] * num_jobs
    first_solution = [[50,51,71,22,23,72,73,74,33,35,34,0,80,10,12,11,1,81,82,90,59,63,56,75,76,64,77,65,67,78,89,79,60,61,62,58,55], [18,21,2,19,3,20,43,44,45,28,29,13,14,15], [24,27,26,25,88,4,16,5,17,70,68,69], [30,32,31,6,48,7,49,46,47,53,54],[38,37,36,39,40,42,41,8,86,85,9,52,87,84,83,66,91,57]]
    machine_comp_times =[45052.87424,53567.404674,35789.78637,42019.52613,45374.55635] #Completion time of machines
    job_comp_times=[22007.602617,28830.04515,25418.182018,32836.363898,21709.39045,32852.24776,27078.2613396,31796.4431106,23074.38084,29686.047484,27488.868666,28830.04515,27959.456906,51623.097474,52458.541974,53567.404674,32852.24776,32937.962047,17563.63651,32836.363898,33215.311274,23978.182018,6079.769306,7483.542864,5941.463479,19024.39045,14634.1465,11853.658665,48018.347834,50018.347874,16826.087265,25638.2613396,19800.000363,17567.602647,20567.602617,18812.047079,10632,5064,3360,16123.666612,20537.238004,23074.38084,23005.809412,36701.849724,37163.388184,40624.926634,36603.6565636,36864.5261336,31796.4431106,34387.3521756,1799.999982,3222.22219,33686.047484,40879.5261336,42019.5261336,45052.8742356041,35555.0899523684,45374.556345,44716.8742356041,32955.511005,43942.8742356041,44134.8742356041,44326.8742356041,34307.0899523684,37274.6551864989,40165.3011026041,44787.714246,41720.3011026041,35227.286367,35789.786367,33382.286367,4266.090095,8588.542864,11359.696701,15098.158227,36232.2638773684,36493.1334473684,39445.5642604989,42371.3880706041,43725.8742356041,23181.515682,31355.04515,31980.04515,42562.714246,36589.380838,25366.047484,23199.380839,34911.047484,20269.39045,42787.6924256041,32147.902295,45128.503716]
    #completion time of jobs
    total_comp=[45804.55639] #Min completion time of machines
    jobs_to_machines=[0,0,1,1,2,2,3,3,4,4,0,0,0,1,1,1,2,2,1,1,1,1,0,0,2,2,2,2,1,1,3,3,3,0,0,0,4,4,4,4,4,4,4,1,1,1,3,3,3,3,0,0,4,3,3,0,0,4,0,0,0,0,0,0,0,0,4,0,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,4,4,2,0,0,4]
    #Which jobs are processed on which machines
    temp_mach_comp_times =[45052.87424,53567.404674,35789.78637,42019.52613,45374.55635]

    print("First solution is : ", first_solution)
    print(" with completion ", machine_comp_times)
    print("max completion time-first ", max(machine_comp_times))

    return first_solution, job_comp_times, jobs_to_machines, temp_mach_comp_times,machine_comp_times

def find_neighborhood(solution, set_up_merging, proc_time,Demand, mode_of_op, num_op):
    num_machs = 5
    num_mach = 5
    num_jobs=92
    mach_to_jobs = solution[0]
    temp_job_comp_times = [0] * num_jobs
    temp_machine_comp_times = [0] * num_mach
    neighborhood_of_solution = []
    assignable_mach= [[0],[0],[1],[1],[2],[2],[3],[3],[4],[4],[0],[0],[0],[0,1,2],[0,1,2],[0,1,2],[2],[2],[0,1,2],[0,1,2],[0,1,2],[0,1,2],
                      [0,1],[0,1],[2],[2],[2],[2],[0,1,2],[0,1,2],[0,1,3],[0,1,3],[0,1,3],[0,1],[0,1],[0,1],[3],[3],[3],[3],[3],[3],[3],[0,1,3],[0,1,3],[0,1,3],[0,1,3],[0,1,3],[3],[3],[0,1],[0,1],[4],[3],[3],
                      [0],[0],[4],[0],[0],[0],[0],[0],[0],[0],[0],[4],[0],[2],[2],[2],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[4],[4],[4],[4],[4],[2],[0],[0],[4]]

    #Which jobs processed on which machines

    neighbor = []
    new_mach_to_jobs = copy.deepcopy(mach_to_jobs)  # new job assignments
    empty_mach = False

    # insertion mode
    inserted = []
    for k in range(0, num_machs):
        m1 = k
        # take k'th machine to get a random job from it to insert somewhere else
        if len(new_mach_to_jobs[m1]) == 0:
            # if there is no job in the machine we can't pick a job from it so continue with next machine
            empty_mach = True
            break
        toplamMakSayisi = 0
        for t in range(0, len(mach_to_jobs[k])):
            job_temp_temporary = mach_to_jobs[k][t]
            toplamMakSayisi += len(assignable_mach[job_temp_temporary])

        if toplamMakSayisi == len(mach_to_jobs[k]):
            break

        temp_mach_to_jobs = new_mach_to_jobs

        j1_ind = random.randint(0, len(new_mach_to_jobs[m1]) - 1) # take a random index from m1
        j1 = new_mach_to_jobs[m1][j1_ind]

        while len(assignable_mach[j1]) == 1:
            # if there is only one machine that the job can be assigned continue
            j1_ind = random.randint(0, len(new_mach_to_jobs[m1]) - 1)

            j1 = new_mach_to_jobs[m1][j1_ind]

        m2= assignable_mach[j1][random.randint(0, len(assignable_mach[j1]) - 1)]
        while m1 == m2:
            m2 = assignable_mach[j1][random.randint(0, len(assignable_mach[j1]) - 1)]

        temp_mach_to_jobs=new_mach_to_jobs


        del new_mach_to_jobs[m1][j1_ind]

        FeasibleDegil = 1
        while FeasibleDegil==1:

            random_loc = random.randint(0, len(new_mach_to_jobs[m2]))  # pick a random location to insert j1 to m2

            new_mach_to_jobs[m2].insert(random_loc,j1)

            mach_to_jobs=new_mach_to_jobs

            new_comp,job_comp_times = calcComp(set_up_merging, proc_time, Demand, mach_to_jobs)
            print("machine: " , k)

            if  job_comp_times[0] < 30240 and job_comp_times[2] < 30240 and job_comp_times[4] < 30240 and job_comp_times[6] < 30240 and job_comp_times[9] < 33120 :

                inserted.append(j1)
                FeasibleDegil=0
            else:
                del new_mach_to_jobs[m2][random_loc]

    if not empty_mach:
        new_comp,job_comp_times = calcComp(set_up_merging, proc_time, Demand, mach_to_jobs)
        neighbor.append(new_mach_to_jobs)
        neighbor.append(inserted)
        neighbor.append(new_comp)
        neighbor.append(job_comp_times)
        neighbor.append(max(new_comp))
        neighborhood_of_solution.append(neighbor)


    indexOfLastItemInTheList = len(neighborhood_of_solution[0]) - 1
    neighborhood_of_solution.sort(key=lambda x: x[indexOfLastItemInTheList])
    return neighborhood_of_solution


def find_neighborhood_second (solution, set_up_merging, proc_time, Demand, num_op):
    num_machs = 5
    mach_to_jobs = solution[0]
    neighborhood_of_solution_second = []
    assignable_mach =[[0],[0],[1],[1],[2],[2],[3],[3],[4],[4],[0],[0],[0],[0,1,2],[0,1,2],[0,1,2],[2],[2],[0,1,2],[0,1,2],[0,1,2],[0,1,2],
                      [0,1],[0,1],[2],[2],[2],[2],[0,1,2],[0,1,2],[0,1,3],[0,1,3],[0,1,3],[0,1],[0,1],[0,1],[3],[3],[3],[3],[3],[3],[3],[0,1,3],[0,1,3],[0,1,3],[0,1,3],[0,1,3],[3],[3],[0,1],[0,1],[4],[3],[3],
                      [0],[0],[4],[0],[0],[0],[0],[0],[0],[0],[0],[4],[0],[2],[2],[2],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[4],[4],[4],[4],[4],[2],[0],[0],[4]]

    for k in range(0, num_machs):

        neighbor_second= []
        second_mach_to_jobs = copy.deepcopy(mach_to_jobs)
        empty_mach = False
        # swap mode
        swapped = []

        for k in range(0, num_machs):
            for op in range(num_op):
                m1 = k
                if len(second_mach_to_jobs[m1]) == 0:
                    empty_mach = True
                    break

                j1_ind = random.randint(0, len(second_mach_to_jobs[m1]) - 1)
                j1 = second_mach_to_jobs[m1][j1_ind]
                del second_mach_to_jobs[m1][j1_ind]

                m2 = random.choice(assignable_mach[j1])
                while len(second_mach_to_jobs[m2]) == 0:
                    m2 = random.choice(assignable_mach[j1_ind])

                j2_ind = random.randint(0, len(second_mach_to_jobs[m2]) - 1)
                j2 = second_mach_to_jobs[m2][j2_ind]
                del second_mach_to_jobs[m2][j2_ind]
                second_mach_to_jobs[m1].insert(j1_ind, j2)
                second_mach_to_jobs[m2].insert(j2_ind, j1)
                swapped.append(j1)
                swapped.append(j2)


    if not empty_mach:
        new_comp,job_comp_times = calcComp(set_up_merging, proc_time, Demand, mach_to_jobs)
        neighbor_second.append(second_mach_to_jobs)
        neighbor_second.append(swapped)
        neighbor_second.append(new_comp)
        neighbor_second.append(job_comp_times)
        neighbor_second.append(max(new_comp))
        neighborhood_of_solution_second.append(neighbor_second)

    indexOfLastItemInTheList = len(neighborhood_of_solution_second[0]) - 1
    neighborhood_of_solution_second.sort(key=lambda x: x[indexOfLastItemInTheList])
    return neighborhood_of_solution_second


def tabu_search(first_solution, set_up_merging, proc_time,Demand, iters, size, asp_chriteria, mode_of_op, num_op):
    count = 1
    solution = first_solution

    tabu_list = list()
    best_cost = max(first_solution[-1])
    best_solution_ever = solution

    while count <= iters:
        neighborhood = find_neighborhood(solution, set_up_merging, proc_time, Demand, mode_of_op, num_op)
        index_of_best_solution = 0
        best_solution = neighborhood[index_of_best_solution]
        print(" ")
        print("Best solution for iteration ", count, " :")
        print("")
        print(best_solution)
        print("")
        best_cost_index = len(best_solution) - 3

        found = False
        if mode_of_op == 1:

            while found is False:
                inserted = best_solution[1]
                tabu_check = False
                for k in range(len(inserted)):
                    if inserted[k] not in tabu_list:
                        tabu_check = True

                if tabu_check:
                    for k in range(len(inserted)):
                        tabu_list.append(inserted[k])

                    found = True
                    solution = best_solution
                    cost = max(neighborhood[index_of_best_solution][best_cost_index])

                    if cost < best_cost:
                        best_cost = cost
                        best_solution_ever = solution

                else:
                    cost = max(neighborhood[index_of_best_solution][best_cost_index])
                    if asp_chriteria and (cost < best_cost):
                        best_cost = cost
                        solution=best_solution
                        best_solution_ever = solution
                        found = True
                    else:
                        index_of_best_solution = index_of_best_solution + 1
                        if (index_of_best_solution == (len(neighborhood))):
                            break
                        best_solution = neighborhood[index_of_best_solution]
            if len(tabu_list) >= size:
                for k in range(num_op):
                    tabu_list.pop(0 + k)
            count = count + 1

    return best_solution_ever, best_cost


def tabu_search_second(first_solution, set_up_merging, proc_time, Demand, iters, size, asp_chriteria,  num_op):
    count = 1
    solution_second = first_solution

    tabu_list_second = list()
    best_cost_second = max(first_solution[1])
    best_solution_ever_second = solution_second
    cost_second=float

    while count <= iters:
        neighborhood_second = find_neighborhood_second(solution_second, set_up_merging, proc_time, Demand,  num_op)
        index_of_best_solution_second = 0
        best_solution_second = neighborhood_second[index_of_best_solution_second]
        print("Best solution for iteration-2 ", count, " :")
        print("")
        print(best_solution_second)
        print("")
        best_cost_index_second = len(best_solution_second) - 1

        found = False
        while found is False:
            swapped = best_solution_second[1]
            if [swapped[0], swapped[1]] not in tabu_list_second and [swapped[1], swapped[0]] not in tabu_list_second:

                tabu_list_second.append([swapped[0], swapped[1]])
                found = True
                solution_second = best_solution_second
                cost_second = neighborhood_second[index_of_best_solution_second][best_cost_index_second]

                if cost_second < best_cost_second:
                    best_cost_second = cost_second
                    best_solution_ever_second = solution_second

            else:
                cost_second= neighborhood_second[index_of_best_solution_second][best_cost_index_second]
                if asp_chriteria and (cost_second < best_cost_second):
                    best_cost_second = cost_second
                    solution_second = best_solution_second
                    best_solution_ever_second = solution_second

                    found = True
                else:

                    index_of_best_solution_second = index_of_best_solution_second + 1
                    if (index_of_best_solution_second == (len(neighborhood_second) - 1)):
                        break
                    best_solution_second = neighborhood_second[index_of_best_solution_second]


        if len(tabu_list_second) >= size:

            for k in range(num_op):
                tabu_list_second.pop(0 + k)
        count = count + 1
    return best_solution_ever_second, best_cost_second

def main():

    tabu_iter = 430
    tabu_size = 5

    asp_chriteria = False
    random_first_sol = True

    mode_of_op = 1
    num_op = 1

    print("Tabu iteration size set to : ", tabu_iter)
    print("Tabu length set to : ", tabu_size)

    set_up=pd.read_excel('Set_up.xlsx').values.tolist()
    set_up_1=[set_up[0],set_up[1],set_up[2],set_up[3],set_up[4],set_up[5],set_up[6],set_up[7],set_up[8],set_up[9],set_up[10],set_up[11],set_up[12] , set_up[13] , set_up[14] , set_up[15] , set_up[16] , set_up[17] , set_up[18] , set_up[19] , set_up[20] , set_up[21] , set_up[22] , set_up[23],set_up[24],set_up[25],set_up[26],set_up[27],set_up[28],set_up[29],set_up[30],set_up[31],set_up[32],set_up[33],set_up[34],set_up[35],set_up[36] ,set_up[37] , set_up[38] ,set_up[39] , set_up[40] , set_up[41] , set_up[42] , set_up[43],set_up[44],set_up[45],set_up[46],set_up[47],set_up[48],set_up[49],set_up[50],set_up[51] , set_up[52] , set_up[53],set_up[54],set_up[55],set_up[56],set_up[57],set_up[58],set_up[59],set_up[60], set_up[61] , set_up[62] , set_up[63],set_up[64],set_up[65],set_up[66],set_up[67],set_up[68],set_up[69],set_up[70], set_up[71], set_up[72], set_up[73],set_up[74],set_up[75],set_up[76],set_up[77],set_up[78],set_up[79],set_up[80], set_up[81] , set_up[82],set_up[83] , set_up[84] , set_up[85] , set_up[86] , set_up[87] , set_up[88] , set_up[89] ,set_up[90] , set_up[91]]
    set_up_2 = [ set_up[92] ,set_up[93] , set_up[94] ,set_up[95] , set_up[96] , set_up[97] , set_up[98] , set_up[99] , set_up[100] , set_up[101] ,set_up[102] ,set_up[103] , set_up[104], set_up[105] , set_up[106] , set_up[107] , set_up[108] ,set_up[109], set_up[110] , set_up[111], set_up[112] , set_up[113] ,set_up[114] , set_up[115] , set_up[116] , set_up[117] , set_up[118] , set_up[119] , set_up[120] , set_up[121] , set_up[122] , set_up[123] , set_up[124] , set_up[125] , set_up[126] , set_up[127] , set_up[128] , set_up[129] , set_up[130] , set_up[131] , set_up[132] , set_up[133] , set_up[134] , set_up[135] , set_up[136] , set_up[137] ,set_up[138], set_up[139] ,set_up[140] , set_up[141] , set_up[142] , set_up[143] , set_up[144] , set_up[145] , set_up[146] , set_up[147] , set_up[148] , set_up[149] , set_up[150] ,set_up[151] , set_up[152] , set_up[153] ,set_up[154] ,set_up[155] ,set_up[156] , set_up[157] , set_up[158],set_up[159] , set_up[160] , set_up[161] , set_up[162] ,set_up[163] ,set_up[164] , set_up[165],set_up[166] , set_up[167] , set_up[168] , set_up[169] , set_up[170], set_up[171] ,set_up[172] , set_up[173] ,set_up[174] ,set_up[175],set_up[176] , set_up[177] ,set_up[178] , set_up[179] , set_up[180] ,set_up[181] , set_up[182] , set_up[183]]
    set_up_3 = [ set_up[184] , set_up[185] , set_up[186] ,set_up[187] ,set_up[188] ,set_up[189],  set_up[190] , set_up[191] , set_up[192] , set_up[193] , set_up[194] , set_up[195] , set_up[196] ,set_up[197] , set_up[198] , set_up[199], set_up[200] ,set_up[201] , set_up[202] , set_up[203] , set_up[204] , set_up[205] , set_up[206] , set_up[207] ,set_up[208] ,set_up[209] ,set_up[210] , set_up[211] , set_up[212] , set_up[213] , set_up[214] ,set_up[215] , set_up[216] , set_up[217] ,set_up[218] , set_up[219] ,set_up[220] ,set_up[221] , set_up[222] , set_up[223], set_up[224] ,set_up[225] , set_up[226] , set_up[227] , set_up[228] ,set_up[229], set_up[230] , set_up[231], set_up[232], set_up[233] , set_up[234] , set_up[235] , set_up[236] , set_up[237], set_up[238] ,set_up[239] , set_up[240] , set_up[241] ,set_up[242] ,set_up[243] ,set_up[244] , set_up[245] ,set_up[246] , set_up[247] , set_up[248],set_up[249] , set_up[250] , set_up[251] , set_up[252] ,set_up[253] , set_up[254] , set_up[255] , set_up[256] , set_up[257],  set_up[258], set_up[259] , set_up[260] , set_up[261] , set_up[262] ,set_up[263] , set_up[264] ,set_up[265], set_up[266], set_up[267] ,set_up[268] , set_up[269] ,set_up[270] , set_up[271] ,set_up[272] , set_up[273] , set_up[274] , set_up[275]]
    set_up_4 =  [ set_up[276] , set_up[277] , set_up[278] , set_up[279] , set_up[280] ,set_up[281] , set_up[282] , set_up[283] , set_up[284] , set_up[285] , set_up[286] , set_up[287] , set_up[288] , set_up[289] , set_up[290] , set_up[291] , set_up[292] ,set_up[293], set_up[294] ,set_up[295] , set_up[296] , set_up[297] ,set_up[298] , set_up[299] , set_up[300] , set_up[301] , set_up[302] , set_up[303] , set_up[304] , set_up[305] ,set_up[306] , set_up[307] , set_up[308] ,set_up[309] ,set_up[310] , set_up[311] ,set_up[312] , set_up[313] , set_up[314] , set_up[315] ,set_up[316] , set_up[317] , set_up[318] ,set_up[319] ,set_up[320] , set_up[321], set_up[322] ,set_up[323], set_up[324] , set_up[325] ,set_up[326] , set_up[327] , set_up[328], set_up[329] , set_up[330] , set_up[331],set_up[332] , set_up[333] , set_up[334] , set_up[335] , set_up[336] , set_up[337] , set_up[338] , set_up[339] , set_up[340],set_up[341] , set_up[342] , set_up[343] , set_up[344] , set_up[345] , set_up[346] , set_up[347] , set_up[348] , set_up[349] , set_up[350] , set_up[351] , set_up[352] , set_up[353] , set_up[354] , set_up[355] , set_up[356] , set_up[357] , set_up[358] , set_up[359] , set_up[360] , set_up[361] , set_up[362] , set_up[363] ,set_up[364] , set_up[365] , set_up[366] , set_up[367]]

    set_up_5 = [ set_up[368] , set_up[369] , set_up[370] , set_up[371] , set_up[372] , set_up[373] , set_up[374] , set_up[375] , set_up[376] , set_up[377] , set_up[378] , set_up[379] , set_up[380] , set_up[381] , set_up[382] , set_up[383] , set_up[384] , set_up[385] , set_up[386] , set_up[387] , set_up[388] , set_up[389] , set_up[390] , set_up[391] , set_up[392] , set_up[393] , set_up[394] , set_up[395] , set_up[396] , set_up[397] , set_up[398] , set_up[399] , set_up[400] , set_up[401] , set_up[402] , set_up[403] , set_up[404] , set_up[405] , set_up[406] , set_up[407] , set_up[408] , set_up[409] , set_up[410] , set_up[411] , set_up[412] , set_up[413] , set_up[414],set_up[415] , set_up[416] , set_up[417] , set_up[418] , set_up[419] , set_up[420] , set_up[421] , set_up[422] , set_up[423] , set_up[424] , set_up[425] , set_up[426] , set_up[427] , set_up[428] , set_up[429] , set_up[430] , set_up[431] , set_up[432] , set_up[433] , set_up[434] , set_up[435] , set_up[436] , set_up[437] , set_up[438] , set_up[439] , set_up[440] , set_up[441] , set_up[442] , set_up[443] , set_up[444] , set_up[445] , set_up[446] , set_up[447] , set_up[448] , set_up[449] , set_up[450] , set_up[451] , set_up[452] , set_up[453] , set_up[454] , set_up[455] , set_up[456] , set_up[457] , set_up[458] , set_up[459]]
    set_up_merging=[set_up_1,set_up_2,set_up_3,set_up_4,set_up_5]


    proc_time = pd.read_excel('Process_times.xlsx').values.tolist()

    Demand= pd.read_excel('Demand.xlsx').values.tolist()

    num_jobs = 92
    num_machs = 5

    start = time.time()
    mach_to_jobs, comp_first_solution, jobs_to_machines,temp_mach_comp_times,machine_comp_times = generate_first_solution(set_up_merging, proc_time, Demand,random_first_sol)
    first_solution = []
    first_solution.append(mach_to_jobs)
    first_solution.append(machine_comp_times)
    neighborhood_of_solution= find_neighborhood(first_solution, set_up_merging, proc_time, Demand, mode_of_op, num_op)
    best_solution, best_cost = tabu_search(first_solution, set_up_merging, proc_time, Demand, tabu_iter, tabu_size, asp_chriteria,mode_of_op, num_op)

    neighborhood_of_solution = find_neighborhood_second(first_solution, set_up_merging, proc_time, Demand,  num_op)

    best_solution_second, best_cost_second = tabu_search_second(first_solution, set_up_merging, proc_time, Demand, tabu_iter, tabu_size,
                                           asp_chriteria, num_op)
    end = time.time()

    print("\n\nBest solution for tabu search is : ")
    print("best_solution", best_solution)
    print(" ")
    print("best_solution_swapping", best_solution_second)

    comp_time_max_comparing=[]
    print("Job assigned to machines: ", best_solution[0])
    print("Total completion time of machines : ", best_solution[2])
    print("Maximum completion time: ", best_solution[4])
    comp_time_max_comparing.append(best_solution[4])

    print("Job assigned to machines: swapping  ", best_solution_second[0])
    print("Total completion time of machines: swapping  ", best_solution_second[2])
    print("Maximum completion time: swapping ", best_solution_second[4])

    comp_time_max_comparing.append(best_solution_second[4])
    print ("BEST min total comp time: ", min(comp_time_max_comparing))
    if min(comp_time_max_comparing)==comp_time_max_comparing[0]:
        print("BEST Job assigned to machines: ", best_solution[0])
        print("BEST Total completion time of machines : ", best_solution[2])
        print("BEST Maximum completion time: ", best_solution[4])

        df = pd.DataFrame(columns=['Job-Mach1', 'Completion Time-Mach1'])

        for t in range(0, len(best_solution[0][0])):
            df = df.append(
                {'Job-Mach1': best_solution[0][0][t], 'Completion Time-Mach1': best_solution[3][best_solution[0][0][t]]},
                ignore_index=True)

        df = df.sort_values(by='Completion Time-Mach1', ascending=True)
        table_result_1 = tabulate(df, headers='keys', tablefmt='psql',showindex=False)


        df_2 = pd.DataFrame(columns=['Job-Mach2', 'Completion Time-Mach2'])

        for h in range(0, len(best_solution[0][1])):
            df_2 = df_2.append(
                {'Job-Mach2': best_solution[0][1][h],
                 'Completion Time-Mach2': best_solution[3][best_solution[0][1][h]]},
                ignore_index=True)

        df_2 = df_2.sort_values(by='Completion Time-Mach2', ascending=True)
        table_result_2 = tabulate(df_2, headers='keys', tablefmt='psql',showindex=False)


        df_3 = pd.DataFrame(columns=['Job-Mach3', 'Completion Time-Mach3'])

        for g in range(0, len(best_solution[0][2])):
            df_3 = df_3.append(
                {'Job-Mach3': best_solution[0][2][g],
                 'Completion Time-Mach3': best_solution[3][best_solution[0][2][g]]},
                ignore_index=True)

        df_3 = df_3.sort_values(by='Completion Time-Mach3', ascending=True)
        table_result_3 = tabulate(df_3, headers='keys', tablefmt='psql',showindex=False)



        df_4 = pd.DataFrame(columns=['Job-Mach4', 'Completion Time-Mach4'])

        for b in range(0, len(best_solution[0][3])):
            df_4= df_4.append(
                {'Job-Mach4': best_solution[0][3][b],
                 'Completion Time-Mach4': best_solution[3][best_solution[0][3][b]]},
                ignore_index=True)

        df_4 = df_4.sort_values(by='Completion Time-Mach4', ascending=True)
        table_result_4 = tabulate(df_4, headers='keys', tablefmt='psql',showindex=False)


        df_5 = pd.DataFrame(columns=['Job-Mach5', 'Completion Time-Mach5'])

        for k in range(0, len(best_solution[0][4])):
            df_5 = df_5.append(
                {'Job-Mach5': best_solution[0][4][k],
                 'Completion Time-Mach5': best_solution[3][best_solution[0][4][k]]},ignore_index=True)

        df_5 = df_5.sort_values(by='Completion Time-Mach5', ascending=True)
        table_result_5 = tabulate(df_5, headers='keys', tablefmt='psql',showindex=False)
        print("TABLE RESULT-5",table_result_1+table_result_2+table_result_3+table_result_4+ table_result_5)


    else:
        print("BEST Job assigned to machines: swapping  ", best_solution_second[0])
        print("BEST Total completion time of machines: swapping  ", best_solution_second[2])
        print("BEST Maximum completion time: swapping ", best_solution_second[4])

        df = pd.DataFrame(columns=['Job-Mach1', 'Completion Time-Mach1'])

        for t in range(0, len(best_solution_second[0][0])):
            df = df.append(
                {'Job-Mach1': best_solution_second[0][0][t], 'Completion Time-Mach1': best_solution_second[3][best_solution_second[0][0][t]]},
                ignore_index=True)

        df = df.sort_values(by='Completion Time-Mach1', ascending=True)
        table_result_1 = tabulate(df, headers='keys', tablefmt='psql',showindex=False)


        df_2 = pd.DataFrame(columns=['Job-Mach2', 'Completion Time-Mach2'])

        for h in range(0, len(best_solution_second[0][1])):
            df_2 = df_2.append(
                {'Job-Mach2': best_solution_second[0][1][h],
                 'Completion Time-Mach2': best_solution_second[3][best_solution_second[0][1][h]]},
                ignore_index=True)

        df_2 = df_2.sort_values(by='Completion Time-Mach2', ascending=True)
        table_result_2 = tabulate(df_2, headers='keys', tablefmt='psql',showindex=False)


        df_3 = pd.DataFrame(columns=['Job-Mach3', 'Completion Time-Mach3'])

        for g in range(0, len(best_solution_second[0][2])):
            df_3 = df_3.append(
                {'Job-Mach3': best_solution_second[0][2][g],
                 'Completion Time-Mach3': best_solution_second[3][best_solution_second[0][2][g]]},
                ignore_index=True)

        df_3 = df_3.sort_values(by='Completion Time-Mach3', ascending=True)
        table_result_3 = tabulate(df_3, headers='keys', tablefmt='psql',showindex=False)


        df_4 = pd.DataFrame(columns=['Job-Mach4', 'Completion Time-Mach4'])

        for b in range(0, len(best_solution_second[0][3])):
            df_4 = df_4.append(
                {'Job-Mach4': best_solution_second[0][3][b],
                 'Completion Time-Mach4': best_solution_second[3][best_solution_second[0][3][b]]},
                ignore_index=True)

        df_4 = df_4.sort_values(by='Completion Time-Mach4', ascending=True)
        table_result_4 = tabulate(df_4, headers='keys', tablefmt='psql',showindex=False)


        df_5 = pd.DataFrame(columns=['Job-Mach5', 'Completion Time-Mach5'])

        for k in range(0, len(best_solution_second[0][4])):
            df_5 = df_5.append(
                {'Job-Mach5': best_solution_second[0][4][k],
                 'Completion Time-Mach5': best_solution_second[3][best_solution_second[0][4][k]]},
                ignore_index=True)

        df_5 = df_5.sort_values(by='Completion Time-Mach5', ascending=True)
        table_result_5 = tabulate(df_5, headers='keys', tablefmt='psql',showindex=False)
        print("TABLE RESULT-5",table_result_1+table_result_2+table_result_3+table_result_4+ table_result_5)

    job_start_times = [0] * num_jobs
    job_end_times = [0] * num_jobs
    mac_curr_times = [0] * num_machs
    time_str = str(end - start)
    time_reformat = time_str[0: time_str.find(".") + 1] + time_str[time_str.find(".") + 1: time_str.find(".") + 3]
    print("Execution time : ", time_reformat, " seconds")


if __name__ == "__main__":
    main()




# In[ ]:


# In[ ]:


# In[ ]:



