---
title: "Report: Week 6 at LLNL"
categories: travel
layout: post
---
For this summer, I came out to Livermore, California to work at Lawrence Livermore National Lab with Dr. Soltz on heavy-ion data and specifically improved detection of jets and jet quenching in heavy-ion collisions. I have just begun my seventh week, which means I have passed the halfway point for the internship. So it seems that now is as good a time as ever to review what I'm working on and what my thoughts at this stage are.

# Research

Initially, the snippet that specified what I would be doing over the summer said "applying Bayesian methods to improve jet detection and understanding of jet quenching in heavy-ion collisions." While this is still the case somewhat, my responsibilities have sort of expanded into other subprojects.

## Jet Quenching Studies

The jet quenching effort is more of a collaborative effort than I initially thought it would be. I work with both my advisor, Dr. Soltz, and a recent full-time hire at the lab working in the same group as me, Dr. Angerami, as well as with a statistician at the lab, Dr. Bulaevskaya. Without going too much into the technical details of the physics problem, in high-energy collisions, jets are a signature that results from hard scattering processes in the initial collision. Jets have many appealing properties that make them particularly interesting to research, but in our case we are interested in how the jet interacts with the quark gluon plasma (QGP) medium as it passes through. In general, we observe a quenching of jet energies which informs us that it does in fact interact. But we want to be able to quantify this and we want to understand which observables are sensitive to in-medium interactions so we can look to those to understand the processes that occur in medium better. Basically, jets offer us a way to look into the properties of the QGP state without just looking at final particle distributions.

My work is part of a bigger effort to develop an approach that would allow the extraction of jet quench factors from experimental data. Currently, I generate hard-scattered (but unquenched) jet events, but choose one jet and manually quench it. This process involved quite a few iterations to make the initial test data as simple and ideal as possible. The goal is to see what methods work on simple data before complicating the data with background or other more difficult hard scatter possibilities. Once a large amount of data is generated for various different quench factors, the data is handed off to Dr. Bulaevskaya, who is primarily responsible for proposing and implementing the methods to re-extract the quench factor from the bulk properties of the events.

## Covariance in High-Energy Data

Another project that became my other focus here is one involving understanding current experimental errors in terms of covariance matrix formalism and making a case for moving to this more general formalism permanently. Effectively, this project involved me replicating results and significance tests from a paper published by the ALICE experiment at CERN, both using traditional chi-squared minimization and using covariance matrices. I have done this successfully, and in the process I think it became clear that the ALICE experiment made some assumptions about the correlations on certain systematic errors that may not have needed to be made if a full covariance matrix was used instead. Regardless of whether this is the case, I was able to demonstrate that covariance matrix algebra can *easily* be used to produce the exact same results as traditional chi-squared minimization.

## High-Energy Data

After demonstrating that covariance matrices are an equivalent and more general way to compute the significance of results, the next step was making sure that the high-energy physics data format (HEPData) had appropriate support for covariance matrices. So my job has involved extending the current schema for the data to support this more general data. While it seems that my simple adjustment to the schema is sufficient to allow the new file with adjusted formatting, I am not satisfied with how permissible it is currently. There need to be more software-level checks to ensure that the data is actually correct (covariance matrix is square and symmetric, etc.). I will probably need to talk to the HEPData developers to understand their approach to this.

# Lab Life

My life at the lab has been great so far. For the past six weeks, I have biked to work usually getting there and starting between 7:30 and 8:30 and leaving sometime between 6:00 and 7:00 in the evening. I have been getting a lot of flats, however, and at least for the near future I plan on walking instead of biking. This will take me an hour each way, roughly, but it will give me a chance to listen to music without it just sitting in the background as I work. At the lab, I generally work out three days a week and typically use my lunch break to play volleyball or go with one of the networking groups. Beyond that, I do not work all day. I actually have the opportunity to attend a variety of meetings and seminars on various topics. The diverse set of things I get to do while at the lab, either while working or on breaks, ensures that I am never bored.

# NorCal Life

Outside of my time at the lab, I actually do relatively little. I chose housing based on not wanting to get/bring a car. As a result, I am restricted to what is accessible to me via walking and public transport. So that and my weekday hours lead me to stay at home weekdays. Only occasionally will I try to make it out of Livermore on the weekend, such as going to Fremont or Union City to meet up with friends. The life here is comfortable; the weather is hot, how I like it, and rain or other bad weather that would make commuting uncomfortable is nowhere to be seen. My housing situation is cheap, and my satisfaction with it reflects that. But I really don't spend much time there, so I have managed to work around my discomfort. I may elaborate on this later, but I also don't want to throw the best efforts of the people that organized and provided my housing under the bus; it's just not how I would choose to live and my lack of control makes me unable to tune it to what I'd like.

Overall, my time in California has been quite nice so far. I've had a good balance of productive work and relaxing free time. In particular, I feel the projects I have been working on are exactly the right scope for how long I will be here. I was scared that I would arrive and not know what I was doing and not get anything done, but based on these past six weeks that won't be the case. Hopefully, the remainder of my time will be as nice as the first half.

