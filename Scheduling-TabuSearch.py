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

    set_up_merging=pd.read_excel('Set_up.xlsx').values.tolist()
  

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



