int is_menu_option(const char *inp, int max);
int are_same_str(const char *str1, const char *str2);

float kg_to_lb(float kg);
float cm_to_ft(float cm);

float cal_eaten(float cal_per_serving, float servings);

float bmr(float kg, float cm, float age, const char gender);
float basal_cal(float bmr, const char level);
float cal_goal(float basal_cal, const char goal);
float bmi(float weight, float height);

const char* explain_activity_level(const char level);
const char* explain_goal(const char goal);
const char* get_gender_str(const char gender);