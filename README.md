# Expedia Travel Analysis & Recommendation System

## Overview

This project builds an end-to-end data platform to analyze user behavior
in the travel industry, identify drivers of booking conversion, and
recommend hotel clusters based on search context and user profile.

The solution combines data engineering, analytics, machine learning, and
business intelligence to support data-driven decision-making for
marketing and product teams.

------------------------------------------------------------------------

## Objectives

-   Understand key factors that influence booking conversion
-   Analyze user behavior across devices and booking contexts
-   Identify high-impact opportunities to improve conversion rates
-   Build a recommendation system for hotel clusters
-   Deliver actionable insights through an interactive dashboard

------------------------------------------------------------------------

## Dataset

-   Source: Expedia Travel Dataset (https://www.kaggle.com/datasets/jacopoferretti/expedia-travel-dataset)
-   Granularity: Event-level user interactions

The dataset includes user behavior, trip characteristics, marketing
channels, and hotel metadata.

------------------------------------------------------------------------

## Data Architecture

### Bronze Layer

-   Raw ingestion from Kaggle
-   1:1 structure with source data
-   No transformations

------------------------------------------------------------------------

### Silver Layer (Data Cleaning & Feature Engineering)

Key transformations:

-   stay_duration
-   advance_booking_days
-   trip_type (solo / family / group)
-   is_family_trip
-   total_guests
-   is_multi_room

------------------------------------------------------------------------

### Gold Layer (Business Aggregations)

Pre-aggregated datasets for analytics:

-   Conversion analysis
-   Booking window segmentation
-   User behavior profiling
-   Destination and cluster performance

------------------------------------------------------------------------

## Data Quality

-   Removed invalid booking windows (negative values)
-   Handled missing distance values
-   Applied minimum volume filters for reliable analysis
-   Ensured consistency across derived features

------------------------------------------------------------------------

## Analytical Approach

Conversion rate: AVG(is_booking)

Opportunity definition: Volume \* (Conversion Overall - Segment
Conversion)

Focus: high-volume segments performing below the average.

------------------------------------------------------------------------

## Dashboard Structure (Tableau)

### Overview

-   High-level performance metrics
-   Conversion rate by device and channel
-   Identification of key performance gaps (e.g., mobile)
-   See here (https://public.tableau.com/app/profile/matheus.benatti/viz/ExpediaTravel/Opportunities?publish=yes)

------------------------------------------------------------------------

### User & Offer

-   Analysis of user intent and booking context
-   Segments:
    -   Booking window
    -   Package vs non-package
    -   Trip type

------------------------------------------------------------------------

### Opportunities

-   Identification of high-impact segments
-   Ranking based on volume and conversion gap

------------------------------------------------------------------------

## Key Insights

-   Conversion remains low (\~8%), with mobile significantly
    underperforming
-   High-intent users (last-minute) convert up to 2x more
-   Non-package bookings show higher conversion
-   Solo travelers convert more efficiently
-   High-volume segments with below-average conversion represent the
    biggest opportunity

------------------------------------------------------------------------

## Business Recommendations

-   Improve mobile booking experience
-   Simplify package offerings
-   Focus on high-traffic segments
-   Use top-performing clusters as benchmarks

------------------------------------------------------------------------

## Machine Learning Model

Objective: Predict most likely hotel_cluster

Performance: - MAP@5: 0.193 - Baseline: 0.050

\~4x improvement over naive approach

------------------------------------------------------------------------

## Tech Stack

-   Python (pandas, scikit-learn, LightGBM)
-   SQL (PostgreSQL)
-   Tableau
-   FastAPI

------------------------------------------------------------------------

## Project Structure

data/ sql/ src/ dashboards/ notebooks/

------------------------------------------------------------------------

## Limitations

-   No pricing or deep intent signals
-   Aggregated analysis may hide user-level patterns
-   Some segments affected by sample size
