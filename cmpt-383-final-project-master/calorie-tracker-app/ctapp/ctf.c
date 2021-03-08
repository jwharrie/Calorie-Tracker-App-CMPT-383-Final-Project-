#include "ctf.h"
#include <string.h>

int is_menu_option(const char *input, int max) {
	if (strlen(input) != 1) return 0;
	char ch = input[0];
	if (ch < '0' || ch > '9') return 0;
	int i = ch - '0';
	if (i < 0 || i >= max) return 0;
	else return 1;
}

int are_same_str(const char *str1, const char *str2) {
	if (strcmp(str1, str2) == 0) return 1;
	else return 0;
}

float kg_to_lb(float kg) {
	return kg * 2.205;
}

float cm_to_ft(float cm) {
	return cm / 100.0 * 3.281;
}


float cal_eaten(float cal_per_serving, float servings) {
	return cal_per_serving * servings;
}

/*
Calculates basic metabolic rate (BMR).
*/
float bmr(float kg, float cm, float age, const char gender) {
	switch (gender) {
		case 'm':
			return (66.0 + 13.7*kg + 5.0*cm - 6.8*age);
		case 'f':
			return (655.0 + 9.6*kg + 1.8*cm - 4.7*age);
	}
}
/*
Calculates base daily energy expenditure based on activity level.
Activity level codes:
	0: sedentary
	1: lightly active (light exercise/sports 1-3 days/week)
	2: moderatetely active (moderate exercise/sports 3-5 days/week)
	3: very active (hard exercise/sports 6-7 days a week) 
	4: extra active (very hard exercise/sports & physical job or 2x training)
*/
float basal_cal(float bmr, const char level) {
	switch (level) {
		case '0':
			return bmr*1.2;
		case '1':
			return bmr*1.375;
		case '2':
			return bmr*1.55;
		case '3':
			return bmr*1.725;
		case '4':
			return bmr*1.9;
	}
}
/*
Calculates amount of calories required to reach weight goal.
Goal codes:
	0: lose 1 kg per week
	1: lose 0.5 kg per week
	2: lose 0.25 kg per week
	3: maintain weight
	4: gain 0.25 kg per week
	5: gain 0.5 kg per week
	6: gain 1 kg per week
*/
float cal_goal(float basal_cal, const char goal) {
	float daily_cal_change = 7700.0 / 7;
	switch (goal) {
		case '0':
			return (basal_cal - daily_cal_change);
		case '1':
			return (basal_cal - (daily_cal_change/2.0));
		case '2':
			return (basal_cal - (daily_cal_change/4.0));
		case '3':
			return basal_cal;
		case '4':
			return (basal_cal + (daily_cal_change/4.0));
		case '5':
			return (basal_cal + (daily_cal_change/2.0));
		case '6':
			return (basal_cal + daily_cal_change);
	}
}
/*
Calculates BMI of person.
*/
float bmi(float kg, float cm) {
	float m2 = cm/100.0;
	m2 *= m2;
	return (kg/m2);
}

/*
Outputs string explaining each activity level.
Activity levels:
	0: sedentary
	1: lightly active (light exercise/sports 1-3 days/week)
	2: moderatetely active (moderate exercise/sports 3-5 days/week)
	3: very active (hard exercise/sports 6-7 days a week) 
	4: extra active (very hard exercise/sports & physical job or 2x training)
*/
const char* explain_activity_level(const char level) {
	switch (level) {
		case '0':
			return "Sedentary";
		case '1':
			return "Lightly active (light exercise/sports 1-3 days/week)";
		case '2':
			return "Moderatetely active (moderate exercise/sports 3-5 days/week)";
		case '3':
			return "Very active (hard exercise/sports 6-7 days a week)";
		case '4':
			return "Extra active (very hard exercise/sports & physical job or 2x training)";
	}
}
/*
Outputs string explaining each goal code.
Goal codes:
	0: lose 1 kg per week
	1: lose 0.5 kg per week
	2: lose 0.25 kg per week
	3: maintain weight
	4: gain 0.25 kg per week
	5: gain 0.5 kg per week
	6: gain 1 kg per week
*/
const char* explain_goal(const char goal) {
	switch(goal) {
		case '0':
			return "Lose 1 kg per week";
		case '1':
			return "Lose 0.5 kg per week";
		case '2':
			return "Lose 0.25 kg per week";
		case '3':
			return "Maintain weight";
		case '4':
			return "Gain 0.25 kg per week";
		case '5':
			return "Gain 0.5 kg per week";
		case '6':
			return "Gain 1 kg per week";
	}
}

const char* get_gender_str(const char gender) {
	switch (gender) {
		case 'm':
			return "Male";
		case 'f':
			return "Female";
	}
}
