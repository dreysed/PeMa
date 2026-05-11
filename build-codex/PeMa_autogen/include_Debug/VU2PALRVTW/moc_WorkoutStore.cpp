/****************************************************************************
** Meta object code from reading C++ file 'WorkoutStore.h'
**
** Created by: The Qt Meta Object Compiler version 69 (Qt 6.10.2)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "../../../../src/backend/WorkoutStore.h"
#include <QtNetwork/QSslError>
#include <QtCore/qmetatype.h>

#include <QtCore/qtmochelpers.h>

#include <memory>


#include <QtCore/qxptype_traits.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'WorkoutStore.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 69
#error "This file was generated using the moc from 6.10.2. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

#ifndef Q_CONSTINIT
#define Q_CONSTINIT
#endif

QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
QT_WARNING_DISABLE_GCC("-Wuseless-cast")
namespace {
struct qt_meta_tag_ZN12WorkoutStoreE_t {};
} // unnamed namespace

template <> constexpr inline auto WorkoutStore::qt_create_metaobjectdata<qt_meta_tag_ZN12WorkoutStoreE_t>()
{
    namespace QMC = QtMocConstants;
    QtMocHelpers::StringRefStorage qt_stringData {
        "WorkoutStore",
        "loginStateChanged",
        "",
        "loginSucceeded",
        "loginFailed",
        "error",
        "loggedOut",
        "sessionExpired",
        "authErrorChanged",
        "athleteLinked",
        "athleteName",
        "athleteLinkFailed",
        "calendarChanged",
        "athletesChanged",
        "selectedAthleteChanged",
        "selectedDateChanged",
        "selectedDayChanged",
        "selectedWorkoutChanged",
        "selectedWorkoutCommentsChanged",
        "analyticsChanged",
        "aiCoachReportChanged",
        "aiCoachPlanApplied",
        "createdWorkouts",
        "createdTemplates",
        "aiCoachChatReply",
        "message",
        "analyticsPeriodChanged",
        "goalsChanged",
        "routesChanged",
        "openAiKeyChanged",
        "stravaStatusChanged",
        "stravaSyncDone",
        "imported",
        "serverUrlChanged",
        "templatesChanged",
        "createDialogOpenChanged",
        "draftChanged",
        "viewModeChanged",
        "errorChanged",
        "busyChanged",
        "workoutCreated",
        "initialLoad",
        "loginUser",
        "email",
        "password",
        "registerUser",
        "name",
        "role",
        "logout",
        "clearAuthError",
        "linkAthlete",
        "athleteEmail",
        "goToToday",
        "prevMonth",
        "nextMonth",
        "selectDate",
        "dateIso",
        "openCreateDialogForDate",
        "cancelCreateDialog",
        "createWorkout",
        "title",
        "category",
        "distanceKm",
        "durationMin",
        "intensity",
        "notes",
        "hiddenFromAthlete",
        "intervalsJson",
        "updateWorkout",
        "id",
        "deleteWorkout",
        "selectWorkout",
        "addComment",
        "text",
        "markWorkoutStatus",
        "workoutId",
        "status",
        "feedback",
        "markWorkoutStatusDetailed",
        "mood",
        "perceivedExertion",
        "saveTemplate",
        "intervals",
        "tags",
        "updateTemplate",
        "deleteTemplate",
        "planFromTemplate",
        "templateId",
        "analyzeAthleteProgress",
        "horizonDays",
        "applyAiCoachPlan",
        "sendAiCoachMessage",
        "canCurrentUserEditAthlete",
        "athleteId",
        "clearError",
        "refresh",
        "createGoal",
        "targetDate",
        "type",
        "targetValue",
        "targetUnit",
        "deleteGoal",
        "importWatchFile",
        "localPath",
        "generateRoute",
        "lat",
        "lon",
        "preferences",
        "buildRouteFromWaypoints",
        "QVariantList",
        "waypoints",
        "deleteRoute",
        "routeId",
        "setOpenAiKey",
        "key",
        "saveStravaCredentials",
        "clientId",
        "clientSecret",
        "openStravaAuthUrl",
        "syncStrava",
        "disconnectStrava",
        "isLoggedIn",
        "currentUserName",
        "currentUserRole",
        "canEditWorkouts",
        "authError",
        "monthLabel",
        "athletes",
        "selectedAthleteId",
        "selectedAthleteName",
        "selectedDateIso",
        "selectedDayLabel",
        "dayCells",
        "selectedDayWorkouts",
        "selectedWorkout",
        "QVariantMap",
        "selectedWorkoutComments",
        "analyticsSummary",
        "aiCoachReport",
        "analyticsPeriod",
        "goals",
        "routes",
        "hasOpenAiKey",
        "stravaConnected",
        "stravaHasClientId",
        "templateLibrary",
        "createDialogOpen",
        "draftDateIso",
        "viewMode",
        "categories",
        "intensities",
        "errorMessage",
        "busy",
        "serverUrl"
    };

    QtMocHelpers::UintData qt_methods {
        // Signal 'loginStateChanged'
        QtMocHelpers::SignalData<void()>(1, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'loginSucceeded'
        QtMocHelpers::SignalData<void()>(3, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'loginFailed'
        QtMocHelpers::SignalData<void(const QString &)>(4, 2, QMC::AccessPublic, QMetaType::Void, {{
            { QMetaType::QString, 5 },
        }}),
        // Signal 'loggedOut'
        QtMocHelpers::SignalData<void()>(6, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'sessionExpired'
        QtMocHelpers::SignalData<void()>(7, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'authErrorChanged'
        QtMocHelpers::SignalData<void()>(8, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'athleteLinked'
        QtMocHelpers::SignalData<void(const QString &)>(9, 2, QMC::AccessPublic, QMetaType::Void, {{
            { QMetaType::QString, 10 },
        }}),
        // Signal 'athleteLinkFailed'
        QtMocHelpers::SignalData<void(const QString &)>(11, 2, QMC::AccessPublic, QMetaType::Void, {{
            { QMetaType::QString, 5 },
        }}),
        // Signal 'calendarChanged'
        QtMocHelpers::SignalData<void()>(12, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'athletesChanged'
        QtMocHelpers::SignalData<void()>(13, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'selectedAthleteChanged'
        QtMocHelpers::SignalData<void()>(14, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'selectedDateChanged'
        QtMocHelpers::SignalData<void()>(15, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'selectedDayChanged'
        QtMocHelpers::SignalData<void()>(16, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'selectedWorkoutChanged'
        QtMocHelpers::SignalData<void()>(17, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'selectedWorkoutCommentsChanged'
        QtMocHelpers::SignalData<void()>(18, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'analyticsChanged'
        QtMocHelpers::SignalData<void()>(19, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'aiCoachReportChanged'
        QtMocHelpers::SignalData<void()>(20, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'aiCoachPlanApplied'
        QtMocHelpers::SignalData<void(int, int)>(21, 2, QMC::AccessPublic, QMetaType::Void, {{
            { QMetaType::Int, 22 }, { QMetaType::Int, 23 },
        }}),
        // Signal 'aiCoachChatReply'
        QtMocHelpers::SignalData<void(const QString &)>(24, 2, QMC::AccessPublic, QMetaType::Void, {{
            { QMetaType::QString, 25 },
        }}),
        // Signal 'analyticsPeriodChanged'
        QtMocHelpers::SignalData<void()>(26, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'goalsChanged'
        QtMocHelpers::SignalData<void()>(27, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'routesChanged'
        QtMocHelpers::SignalData<void()>(28, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'openAiKeyChanged'
        QtMocHelpers::SignalData<void()>(29, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'stravaStatusChanged'
        QtMocHelpers::SignalData<void()>(30, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'stravaSyncDone'
        QtMocHelpers::SignalData<void(int)>(31, 2, QMC::AccessPublic, QMetaType::Void, {{
            { QMetaType::Int, 32 },
        }}),
        // Signal 'serverUrlChanged'
        QtMocHelpers::SignalData<void()>(33, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'templatesChanged'
        QtMocHelpers::SignalData<void()>(34, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'createDialogOpenChanged'
        QtMocHelpers::SignalData<void()>(35, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'draftChanged'
        QtMocHelpers::SignalData<void()>(36, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'viewModeChanged'
        QtMocHelpers::SignalData<void()>(37, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'errorChanged'
        QtMocHelpers::SignalData<void(const QString &)>(38, 2, QMC::AccessPublic, QMetaType::Void, {{
            { QMetaType::QString, 25 },
        }}),
        // Signal 'busyChanged'
        QtMocHelpers::SignalData<void()>(39, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'workoutCreated'
        QtMocHelpers::SignalData<void()>(40, 2, QMC::AccessPublic, QMetaType::Void),
        // Slot 'initialLoad'
        QtMocHelpers::SlotData<void()>(41, 2, QMC::AccessPrivate, QMetaType::Void),
        // Method 'loginUser'
        QtMocHelpers::MethodData<void(const QString &, const QString &)>(42, 2, QMC::AccessPublic, QMetaType::Void, {{
            { QMetaType::QString, 43 }, { QMetaType::QString, 44 },
        }}),
        // Method 'registerUser'
        QtMocHelpers::MethodData<void(const QString &, const QString &, const QString &, const QString &)>(45, 2, QMC::AccessPublic, QMetaType::Void, {{
            { QMetaType::QString, 43 }, { QMetaType::QString, 46 }, { QMetaType::QString, 44 }, { QMetaType::QString, 47 },
        }}),
        // Method 'logout'
        QtMocHelpers::MethodData<void()>(48, 2, QMC::AccessPublic, QMetaType::Void),
        // Method 'clearAuthError'
        QtMocHelpers::MethodData<void()>(49, 2, QMC::AccessPublic, QMetaType::Void),
        // Method 'linkAthlete'
        QtMocHelpers::MethodData<void(const QString &)>(50, 2, QMC::AccessPublic, QMetaType::Void, {{
            { QMetaType::QString, 51 },
        }}),
        // Method 'goToToday'
        QtMocHelpers::MethodData<void()>(52, 2, QMC::AccessPublic, QMetaType::Void),
        // Method 'prevMonth'
        QtMocHelpers::MethodData<void()>(53, 2, QMC::AccessPublic, QMetaType::Void),
        // Method 'nextMonth'
        QtMocHelpers::MethodData<void()>(54, 2, QMC::AccessPublic, QMetaType::Void),
        // Method 'selectDate'
        QtMocHelpers::MethodData<void(const QString &)>(55, 2, QMC::AccessPublic, QMetaType::Void, {{
            { QMetaType::QString, 56 },
        }}),
        // Method 'openCreateDialogForDate'
        QtMocHelpers::MethodData<void(const QString &)>(57, 2, QMC::AccessPublic, QMetaType::Void, {{
            { QMetaType::QString, 56 },
        }}),
        // Method 'cancelCreateDialog'
        QtMocHelpers::MethodData<void()>(58, 2, QMC::AccessPublic, QMetaType::Void),
        // Method 'createWorkout'
        QtMocHelpers::MethodData<bool(const QString &, const QString &, double, int, const QString &, const QString &, bool, const QString &)>(59, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { QMetaType::QString, 60 }, { QMetaType::QString, 61 }, { QMetaType::Double, 62 }, { QMetaType::Int, 63 },
            { QMetaType::QString, 64 }, { QMetaType::QString, 65 }, { QMetaType::Bool, 66 }, { QMetaType::QString, 67 },
        }}),
        // Method 'createWorkout'
        QtMocHelpers::MethodData<bool(const QString &, const QString &, double, int, const QString &, const QString &, bool)>(59, 2, QMC::AccessPublic | QMC::MethodCloned, QMetaType::Bool, {{
            { QMetaType::QString, 60 }, { QMetaType::QString, 61 }, { QMetaType::Double, 62 }, { QMetaType::Int, 63 },
            { QMetaType::QString, 64 }, { QMetaType::QString, 65 }, { QMetaType::Bool, 66 },
        }}),
        // Method 'createWorkout'
        QtMocHelpers::MethodData<bool(const QString &, const QString &, double, int, const QString &, const QString &)>(59, 2, QMC::AccessPublic | QMC::MethodCloned, QMetaType::Bool, {{
            { QMetaType::QString, 60 }, { QMetaType::QString, 61 }, { QMetaType::Double, 62 }, { QMetaType::Int, 63 },
            { QMetaType::QString, 64 }, { QMetaType::QString, 65 },
        }}),
        // Method 'updateWorkout'
        QtMocHelpers::MethodData<bool(const QString &, const QString &, const QString &, double, int, const QString &, const QString &, bool, const QString &)>(68, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { QMetaType::QString, 69 }, { QMetaType::QString, 60 }, { QMetaType::QString, 61 }, { QMetaType::Double, 62 },
            { QMetaType::Int, 63 }, { QMetaType::QString, 64 }, { QMetaType::QString, 65 }, { QMetaType::Bool, 66 },
            { QMetaType::QString, 67 },
        }}),
        // Method 'updateWorkout'
        QtMocHelpers::MethodData<bool(const QString &, const QString &, const QString &, double, int, const QString &, const QString &, bool)>(68, 2, QMC::AccessPublic | QMC::MethodCloned, QMetaType::Bool, {{
            { QMetaType::QString, 69 }, { QMetaType::QString, 60 }, { QMetaType::QString, 61 }, { QMetaType::Double, 62 },
            { QMetaType::Int, 63 }, { QMetaType::QString, 64 }, { QMetaType::QString, 65 }, { QMetaType::Bool, 66 },
        }}),
        // Method 'updateWorkout'
        QtMocHelpers::MethodData<bool(const QString &, const QString &, const QString &, double, int, const QString &, const QString &)>(68, 2, QMC::AccessPublic | QMC::MethodCloned, QMetaType::Bool, {{
            { QMetaType::QString, 69 }, { QMetaType::QString, 60 }, { QMetaType::QString, 61 }, { QMetaType::Double, 62 },
            { QMetaType::Int, 63 }, { QMetaType::QString, 64 }, { QMetaType::QString, 65 },
        }}),
        // Method 'deleteWorkout'
        QtMocHelpers::MethodData<bool(const QString &)>(70, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { QMetaType::QString, 69 },
        }}),
        // Method 'selectWorkout'
        QtMocHelpers::MethodData<void(const QString &)>(71, 2, QMC::AccessPublic, QMetaType::Void, {{
            { QMetaType::QString, 69 },
        }}),
        // Method 'addComment'
        QtMocHelpers::MethodData<bool(const QString &)>(72, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { QMetaType::QString, 73 },
        }}),
        // Method 'markWorkoutStatus'
        QtMocHelpers::MethodData<bool(const QString &, const QString &, const QString &)>(74, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { QMetaType::QString, 75 }, { QMetaType::QString, 76 }, { QMetaType::QString, 77 },
        }}),
        // Method 'markWorkoutStatusDetailed'
        QtMocHelpers::MethodData<bool(const QString &, const QString &, const QString &, const QString &, int)>(78, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { QMetaType::QString, 75 }, { QMetaType::QString, 76 }, { QMetaType::QString, 77 }, { QMetaType::QString, 79 },
            { QMetaType::Int, 80 },
        }}),
        // Method 'saveTemplate'
        QtMocHelpers::MethodData<bool(const QString &, const QString &, double, int, const QString &, const QString &, const QString &, const QString &)>(81, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { QMetaType::QString, 60 }, { QMetaType::QString, 61 }, { QMetaType::Double, 62 }, { QMetaType::Int, 63 },
            { QMetaType::QString, 64 }, { QMetaType::QString, 82 }, { QMetaType::QString, 65 }, { QMetaType::QString, 83 },
        }}),
        // Method 'updateTemplate'
        QtMocHelpers::MethodData<bool(const QString &, const QString &, const QString &, double, int, const QString &, const QString &, const QString &, const QString &)>(84, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { QMetaType::QString, 69 }, { QMetaType::QString, 60 }, { QMetaType::QString, 61 }, { QMetaType::Double, 62 },
            { QMetaType::Int, 63 }, { QMetaType::QString, 64 }, { QMetaType::QString, 82 }, { QMetaType::QString, 65 },
            { QMetaType::QString, 83 },
        }}),
        // Method 'deleteTemplate'
        QtMocHelpers::MethodData<bool(const QString &)>(85, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { QMetaType::QString, 69 },
        }}),
        // Method 'planFromTemplate'
        QtMocHelpers::MethodData<bool(const QString &, const QString &)>(86, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { QMetaType::QString, 87 }, { QMetaType::QString, 56 },
        }}),
        // Method 'analyzeAthleteProgress'
        QtMocHelpers::MethodData<void(int)>(88, 2, QMC::AccessPublic, QMetaType::Void, {{
            { QMetaType::Int, 89 },
        }}),
        // Method 'analyzeAthleteProgress'
        QtMocHelpers::MethodData<void()>(88, 2, QMC::AccessPublic | QMC::MethodCloned, QMetaType::Void),
        // Method 'applyAiCoachPlan'
        QtMocHelpers::MethodData<void(int)>(90, 2, QMC::AccessPublic, QMetaType::Void, {{
            { QMetaType::Int, 89 },
        }}),
        // Method 'applyAiCoachPlan'
        QtMocHelpers::MethodData<void()>(90, 2, QMC::AccessPublic | QMC::MethodCloned, QMetaType::Void),
        // Method 'sendAiCoachMessage'
        QtMocHelpers::MethodData<void(const QString &, int)>(91, 2, QMC::AccessPublic, QMetaType::Void, {{
            { QMetaType::QString, 25 }, { QMetaType::Int, 89 },
        }}),
        // Method 'sendAiCoachMessage'
        QtMocHelpers::MethodData<void(const QString &)>(91, 2, QMC::AccessPublic | QMC::MethodCloned, QMetaType::Void, {{
            { QMetaType::QString, 25 },
        }}),
        // Method 'canCurrentUserEditAthlete'
        QtMocHelpers::MethodData<bool(const QString &) const>(92, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { QMetaType::QString, 93 },
        }}),
        // Method 'clearError'
        QtMocHelpers::MethodData<void()>(94, 2, QMC::AccessPublic, QMetaType::Void),
        // Method 'refresh'
        QtMocHelpers::MethodData<void()>(95, 2, QMC::AccessPublic, QMetaType::Void),
        // Method 'createGoal'
        QtMocHelpers::MethodData<bool(const QString &, const QString &, const QString &, double, const QString &)>(96, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { QMetaType::QString, 60 }, { QMetaType::QString, 97 }, { QMetaType::QString, 98 }, { QMetaType::Double, 99 },
            { QMetaType::QString, 100 },
        }}),
        // Method 'deleteGoal'
        QtMocHelpers::MethodData<bool(const QString &)>(101, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { QMetaType::QString, 69 },
        }}),
        // Method 'importWatchFile'
        QtMocHelpers::MethodData<bool(const QString &, const QString &)>(102, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { QMetaType::QString, 75 }, { QMetaType::QString, 103 },
        }}),
        // Method 'generateRoute'
        QtMocHelpers::MethodData<void(double, double, double, const QString &)>(104, 2, QMC::AccessPublic, QMetaType::Void, {{
            { QMetaType::Double, 105 }, { QMetaType::Double, 106 }, { QMetaType::Double, 62 }, { QMetaType::QString, 107 },
        }}),
        // Method 'buildRouteFromWaypoints'
        QtMocHelpers::MethodData<void(const QVariantList &, const QString &)>(108, 2, QMC::AccessPublic, QMetaType::Void, {{
            { 0x80000000 | 109, 110 }, { QMetaType::QString, 46 },
        }}),
        // Method 'deleteRoute'
        QtMocHelpers::MethodData<void(const QString &)>(111, 2, QMC::AccessPublic, QMetaType::Void, {{
            { QMetaType::QString, 112 },
        }}),
        // Method 'setOpenAiKey'
        QtMocHelpers::MethodData<void(const QString &)>(113, 2, QMC::AccessPublic, QMetaType::Void, {{
            { QMetaType::QString, 114 },
        }}),
        // Method 'saveStravaCredentials'
        QtMocHelpers::MethodData<void(const QString &, const QString &)>(115, 2, QMC::AccessPublic, QMetaType::Void, {{
            { QMetaType::QString, 116 }, { QMetaType::QString, 117 },
        }}),
        // Method 'openStravaAuthUrl'
        QtMocHelpers::MethodData<void()>(118, 2, QMC::AccessPublic, QMetaType::Void),
        // Method 'syncStrava'
        QtMocHelpers::MethodData<void()>(119, 2, QMC::AccessPublic, QMetaType::Void),
        // Method 'disconnectStrava'
        QtMocHelpers::MethodData<void()>(120, 2, QMC::AccessPublic, QMetaType::Void),
    };
    QtMocHelpers::UintData qt_properties {
        // property 'isLoggedIn'
        QtMocHelpers::PropertyData<bool>(121, QMetaType::Bool, QMC::DefaultPropertyFlags, 0),
        // property 'currentUserName'
        QtMocHelpers::PropertyData<QString>(122, QMetaType::QString, QMC::DefaultPropertyFlags, 0),
        // property 'currentUserRole'
        QtMocHelpers::PropertyData<QString>(123, QMetaType::QString, QMC::DefaultPropertyFlags, 0),
        // property 'canEditWorkouts'
        QtMocHelpers::PropertyData<bool>(124, QMetaType::Bool, QMC::DefaultPropertyFlags, 0),
        // property 'authError'
        QtMocHelpers::PropertyData<QString>(125, QMetaType::QString, QMC::DefaultPropertyFlags, 5),
        // property 'monthLabel'
        QtMocHelpers::PropertyData<QString>(126, QMetaType::QString, QMC::DefaultPropertyFlags, 8),
        // property 'athletes'
        QtMocHelpers::PropertyData<QVariantList>(127, 0x80000000 | 109, QMC::DefaultPropertyFlags | QMC::EnumOrFlag, 9),
        // property 'selectedAthleteId'
        QtMocHelpers::PropertyData<QString>(128, QMetaType::QString, QMC::DefaultPropertyFlags | QMC::Writable | QMC::StdCppSet, 10),
        // property 'selectedAthleteName'
        QtMocHelpers::PropertyData<QString>(129, QMetaType::QString, QMC::DefaultPropertyFlags, 10),
        // property 'selectedDateIso'
        QtMocHelpers::PropertyData<QString>(130, QMetaType::QString, QMC::DefaultPropertyFlags, 11),
        // property 'selectedDayLabel'
        QtMocHelpers::PropertyData<QString>(131, QMetaType::QString, QMC::DefaultPropertyFlags, 11),
        // property 'dayCells'
        QtMocHelpers::PropertyData<QVariantList>(132, 0x80000000 | 109, QMC::DefaultPropertyFlags | QMC::EnumOrFlag, 8),
        // property 'selectedDayWorkouts'
        QtMocHelpers::PropertyData<QVariantList>(133, 0x80000000 | 109, QMC::DefaultPropertyFlags | QMC::EnumOrFlag, 12),
        // property 'selectedWorkout'
        QtMocHelpers::PropertyData<QVariantMap>(134, 0x80000000 | 135, QMC::DefaultPropertyFlags | QMC::EnumOrFlag, 13),
        // property 'selectedWorkoutComments'
        QtMocHelpers::PropertyData<QVariantList>(136, 0x80000000 | 109, QMC::DefaultPropertyFlags | QMC::EnumOrFlag, 14),
        // property 'analyticsSummary'
        QtMocHelpers::PropertyData<QVariantMap>(137, 0x80000000 | 135, QMC::DefaultPropertyFlags | QMC::EnumOrFlag, 15),
        // property 'aiCoachReport'
        QtMocHelpers::PropertyData<QVariantMap>(138, 0x80000000 | 135, QMC::DefaultPropertyFlags | QMC::EnumOrFlag, 16),
        // property 'analyticsPeriod'
        QtMocHelpers::PropertyData<QString>(139, QMetaType::QString, QMC::DefaultPropertyFlags | QMC::Writable | QMC::StdCppSet, 19),
        // property 'goals'
        QtMocHelpers::PropertyData<QVariantList>(140, 0x80000000 | 109, QMC::DefaultPropertyFlags | QMC::EnumOrFlag, 20),
        // property 'routes'
        QtMocHelpers::PropertyData<QVariantList>(141, 0x80000000 | 109, QMC::DefaultPropertyFlags | QMC::EnumOrFlag, 21),
        // property 'hasOpenAiKey'
        QtMocHelpers::PropertyData<bool>(142, QMetaType::Bool, QMC::DefaultPropertyFlags, 22),
        // property 'stravaConnected'
        QtMocHelpers::PropertyData<bool>(143, QMetaType::Bool, QMC::DefaultPropertyFlags, 23),
        // property 'stravaHasClientId'
        QtMocHelpers::PropertyData<bool>(144, QMetaType::Bool, QMC::DefaultPropertyFlags, 23),
        // property 'templateLibrary'
        QtMocHelpers::PropertyData<QVariantList>(145, 0x80000000 | 109, QMC::DefaultPropertyFlags | QMC::EnumOrFlag, 26),
        // property 'createDialogOpen'
        QtMocHelpers::PropertyData<bool>(146, QMetaType::Bool, QMC::DefaultPropertyFlags | QMC::Writable | QMC::StdCppSet, 27),
        // property 'draftDateIso'
        QtMocHelpers::PropertyData<QString>(147, QMetaType::QString, QMC::DefaultPropertyFlags, 28),
        // property 'viewMode'
        QtMocHelpers::PropertyData<QString>(148, QMetaType::QString, QMC::DefaultPropertyFlags | QMC::Writable | QMC::StdCppSet, 29),
        // property 'categories'
        QtMocHelpers::PropertyData<QStringList>(149, QMetaType::QStringList, QMC::DefaultPropertyFlags | QMC::Constant),
        // property 'intensities'
        QtMocHelpers::PropertyData<QStringList>(150, QMetaType::QStringList, QMC::DefaultPropertyFlags | QMC::Constant),
        // property 'errorMessage'
        QtMocHelpers::PropertyData<QString>(151, QMetaType::QString, QMC::DefaultPropertyFlags, 30),
        // property 'busy'
        QtMocHelpers::PropertyData<bool>(152, QMetaType::Bool, QMC::DefaultPropertyFlags, 31),
        // property 'serverUrl'
        QtMocHelpers::PropertyData<QString>(153, QMetaType::QString, QMC::DefaultPropertyFlags | QMC::Writable | QMC::StdCppSet, 25),
    };
    QtMocHelpers::UintData qt_enums {
    };
    return QtMocHelpers::metaObjectData<WorkoutStore, qt_meta_tag_ZN12WorkoutStoreE_t>(QMC::MetaObjectFlag{}, qt_stringData,
            qt_methods, qt_properties, qt_enums);
}
Q_CONSTINIT const QMetaObject WorkoutStore::staticMetaObject = { {
    QMetaObject::SuperData::link<QObject::staticMetaObject>(),
    qt_staticMetaObjectStaticContent<qt_meta_tag_ZN12WorkoutStoreE_t>.stringdata,
    qt_staticMetaObjectStaticContent<qt_meta_tag_ZN12WorkoutStoreE_t>.data,
    qt_static_metacall,
    nullptr,
    qt_staticMetaObjectRelocatingContent<qt_meta_tag_ZN12WorkoutStoreE_t>.metaTypes,
    nullptr
} };

void WorkoutStore::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    auto *_t = static_cast<WorkoutStore *>(_o);
    if (_c == QMetaObject::InvokeMetaMethod) {
        switch (_id) {
        case 0: _t->loginStateChanged(); break;
        case 1: _t->loginSucceeded(); break;
        case 2: _t->loginFailed((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1]))); break;
        case 3: _t->loggedOut(); break;
        case 4: _t->sessionExpired(); break;
        case 5: _t->authErrorChanged(); break;
        case 6: _t->athleteLinked((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1]))); break;
        case 7: _t->athleteLinkFailed((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1]))); break;
        case 8: _t->calendarChanged(); break;
        case 9: _t->athletesChanged(); break;
        case 10: _t->selectedAthleteChanged(); break;
        case 11: _t->selectedDateChanged(); break;
        case 12: _t->selectedDayChanged(); break;
        case 13: _t->selectedWorkoutChanged(); break;
        case 14: _t->selectedWorkoutCommentsChanged(); break;
        case 15: _t->analyticsChanged(); break;
        case 16: _t->aiCoachReportChanged(); break;
        case 17: _t->aiCoachPlanApplied((*reinterpret_cast<std::add_pointer_t<int>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<int>>(_a[2]))); break;
        case 18: _t->aiCoachChatReply((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1]))); break;
        case 19: _t->analyticsPeriodChanged(); break;
        case 20: _t->goalsChanged(); break;
        case 21: _t->routesChanged(); break;
        case 22: _t->openAiKeyChanged(); break;
        case 23: _t->stravaStatusChanged(); break;
        case 24: _t->stravaSyncDone((*reinterpret_cast<std::add_pointer_t<int>>(_a[1]))); break;
        case 25: _t->serverUrlChanged(); break;
        case 26: _t->templatesChanged(); break;
        case 27: _t->createDialogOpenChanged(); break;
        case 28: _t->draftChanged(); break;
        case 29: _t->viewModeChanged(); break;
        case 30: _t->errorChanged((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1]))); break;
        case 31: _t->busyChanged(); break;
        case 32: _t->workoutCreated(); break;
        case 33: _t->initialLoad(); break;
        case 34: _t->loginUser((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[2]))); break;
        case 35: _t->registerUser((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[2])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[3])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[4]))); break;
        case 36: _t->logout(); break;
        case 37: _t->clearAuthError(); break;
        case 38: _t->linkAthlete((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1]))); break;
        case 39: _t->goToToday(); break;
        case 40: _t->prevMonth(); break;
        case 41: _t->nextMonth(); break;
        case 42: _t->selectDate((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1]))); break;
        case 43: _t->openCreateDialogForDate((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1]))); break;
        case 44: _t->cancelCreateDialog(); break;
        case 45: { bool _r = _t->createWorkout((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[2])),(*reinterpret_cast<std::add_pointer_t<double>>(_a[3])),(*reinterpret_cast<std::add_pointer_t<int>>(_a[4])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[5])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[6])),(*reinterpret_cast<std::add_pointer_t<bool>>(_a[7])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[8])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 46: { bool _r = _t->createWorkout((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[2])),(*reinterpret_cast<std::add_pointer_t<double>>(_a[3])),(*reinterpret_cast<std::add_pointer_t<int>>(_a[4])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[5])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[6])),(*reinterpret_cast<std::add_pointer_t<bool>>(_a[7])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 47: { bool _r = _t->createWorkout((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[2])),(*reinterpret_cast<std::add_pointer_t<double>>(_a[3])),(*reinterpret_cast<std::add_pointer_t<int>>(_a[4])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[5])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[6])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 48: { bool _r = _t->updateWorkout((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[2])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[3])),(*reinterpret_cast<std::add_pointer_t<double>>(_a[4])),(*reinterpret_cast<std::add_pointer_t<int>>(_a[5])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[6])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[7])),(*reinterpret_cast<std::add_pointer_t<bool>>(_a[8])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[9])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 49: { bool _r = _t->updateWorkout((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[2])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[3])),(*reinterpret_cast<std::add_pointer_t<double>>(_a[4])),(*reinterpret_cast<std::add_pointer_t<int>>(_a[5])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[6])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[7])),(*reinterpret_cast<std::add_pointer_t<bool>>(_a[8])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 50: { bool _r = _t->updateWorkout((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[2])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[3])),(*reinterpret_cast<std::add_pointer_t<double>>(_a[4])),(*reinterpret_cast<std::add_pointer_t<int>>(_a[5])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[6])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[7])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 51: { bool _r = _t->deleteWorkout((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 52: _t->selectWorkout((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1]))); break;
        case 53: { bool _r = _t->addComment((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 54: { bool _r = _t->markWorkoutStatus((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[2])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[3])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 55: { bool _r = _t->markWorkoutStatusDetailed((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[2])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[3])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[4])),(*reinterpret_cast<std::add_pointer_t<int>>(_a[5])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 56: { bool _r = _t->saveTemplate((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[2])),(*reinterpret_cast<std::add_pointer_t<double>>(_a[3])),(*reinterpret_cast<std::add_pointer_t<int>>(_a[4])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[5])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[6])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[7])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[8])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 57: { bool _r = _t->updateTemplate((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[2])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[3])),(*reinterpret_cast<std::add_pointer_t<double>>(_a[4])),(*reinterpret_cast<std::add_pointer_t<int>>(_a[5])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[6])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[7])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[8])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[9])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 58: { bool _r = _t->deleteTemplate((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 59: { bool _r = _t->planFromTemplate((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[2])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 60: _t->analyzeAthleteProgress((*reinterpret_cast<std::add_pointer_t<int>>(_a[1]))); break;
        case 61: _t->analyzeAthleteProgress(); break;
        case 62: _t->applyAiCoachPlan((*reinterpret_cast<std::add_pointer_t<int>>(_a[1]))); break;
        case 63: _t->applyAiCoachPlan(); break;
        case 64: _t->sendAiCoachMessage((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<int>>(_a[2]))); break;
        case 65: _t->sendAiCoachMessage((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1]))); break;
        case 66: { bool _r = _t->canCurrentUserEditAthlete((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 67: _t->clearError(); break;
        case 68: _t->refresh(); break;
        case 69: { bool _r = _t->createGoal((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[2])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[3])),(*reinterpret_cast<std::add_pointer_t<double>>(_a[4])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[5])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 70: { bool _r = _t->deleteGoal((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 71: { bool _r = _t->importWatchFile((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[2])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 72: _t->generateRoute((*reinterpret_cast<std::add_pointer_t<double>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<double>>(_a[2])),(*reinterpret_cast<std::add_pointer_t<double>>(_a[3])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[4]))); break;
        case 73: _t->buildRouteFromWaypoints((*reinterpret_cast<std::add_pointer_t<QVariantList>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[2]))); break;
        case 74: _t->deleteRoute((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1]))); break;
        case 75: _t->setOpenAiKey((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1]))); break;
        case 76: _t->saveStravaCredentials((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[2]))); break;
        case 77: _t->openStravaAuthUrl(); break;
        case 78: _t->syncStrava(); break;
        case 79: _t->disconnectStrava(); break;
        default: ;
        }
    }
    if (_c == QMetaObject::IndexOfMethod) {
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::loginStateChanged, 0))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::loginSucceeded, 1))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)(const QString & )>(_a, &WorkoutStore::loginFailed, 2))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::loggedOut, 3))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::sessionExpired, 4))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::authErrorChanged, 5))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)(const QString & )>(_a, &WorkoutStore::athleteLinked, 6))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)(const QString & )>(_a, &WorkoutStore::athleteLinkFailed, 7))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::calendarChanged, 8))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::athletesChanged, 9))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::selectedAthleteChanged, 10))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::selectedDateChanged, 11))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::selectedDayChanged, 12))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::selectedWorkoutChanged, 13))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::selectedWorkoutCommentsChanged, 14))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::analyticsChanged, 15))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::aiCoachReportChanged, 16))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)(int , int )>(_a, &WorkoutStore::aiCoachPlanApplied, 17))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)(const QString & )>(_a, &WorkoutStore::aiCoachChatReply, 18))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::analyticsPeriodChanged, 19))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::goalsChanged, 20))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::routesChanged, 21))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::openAiKeyChanged, 22))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::stravaStatusChanged, 23))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)(int )>(_a, &WorkoutStore::stravaSyncDone, 24))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::serverUrlChanged, 25))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::templatesChanged, 26))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::createDialogOpenChanged, 27))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::draftChanged, 28))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::viewModeChanged, 29))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)(const QString & )>(_a, &WorkoutStore::errorChanged, 30))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::busyChanged, 31))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::workoutCreated, 32))
            return;
    }
    if (_c == QMetaObject::ReadProperty) {
        void *_v = _a[0];
        switch (_id) {
        case 0: *reinterpret_cast<bool*>(_v) = _t->isLoggedIn(); break;
        case 1: *reinterpret_cast<QString*>(_v) = _t->currentUserName(); break;
        case 2: *reinterpret_cast<QString*>(_v) = _t->currentUserRole(); break;
        case 3: *reinterpret_cast<bool*>(_v) = _t->canEditWorkouts(); break;
        case 4: *reinterpret_cast<QString*>(_v) = _t->authError(); break;
        case 5: *reinterpret_cast<QString*>(_v) = _t->monthLabel(); break;
        case 6: *reinterpret_cast<QVariantList*>(_v) = _t->athletes(); break;
        case 7: *reinterpret_cast<QString*>(_v) = _t->selectedAthleteId(); break;
        case 8: *reinterpret_cast<QString*>(_v) = _t->selectedAthleteName(); break;
        case 9: *reinterpret_cast<QString*>(_v) = _t->selectedDateIso(); break;
        case 10: *reinterpret_cast<QString*>(_v) = _t->selectedDayLabel(); break;
        case 11: *reinterpret_cast<QVariantList*>(_v) = _t->dayCells(); break;
        case 12: *reinterpret_cast<QVariantList*>(_v) = _t->selectedDayWorkouts(); break;
        case 13: *reinterpret_cast<QVariantMap*>(_v) = _t->selectedWorkout(); break;
        case 14: *reinterpret_cast<QVariantList*>(_v) = _t->selectedWorkoutComments(); break;
        case 15: *reinterpret_cast<QVariantMap*>(_v) = _t->analyticsSummary(); break;
        case 16: *reinterpret_cast<QVariantMap*>(_v) = _t->aiCoachReport(); break;
        case 17: *reinterpret_cast<QString*>(_v) = _t->analyticsPeriod(); break;
        case 18: *reinterpret_cast<QVariantList*>(_v) = _t->goals(); break;
        case 19: *reinterpret_cast<QVariantList*>(_v) = _t->routes(); break;
        case 20: *reinterpret_cast<bool*>(_v) = _t->hasOpenAiKey(); break;
        case 21: *reinterpret_cast<bool*>(_v) = _t->stravaConnected(); break;
        case 22: *reinterpret_cast<bool*>(_v) = _t->stravaHasClientId(); break;
        case 23: *reinterpret_cast<QVariantList*>(_v) = _t->templateLibrary(); break;
        case 24: *reinterpret_cast<bool*>(_v) = _t->createDialogOpen(); break;
        case 25: *reinterpret_cast<QString*>(_v) = _t->draftDateIso(); break;
        case 26: *reinterpret_cast<QString*>(_v) = _t->viewMode(); break;
        case 27: *reinterpret_cast<QStringList*>(_v) = _t->categories(); break;
        case 28: *reinterpret_cast<QStringList*>(_v) = _t->intensities(); break;
        case 29: *reinterpret_cast<QString*>(_v) = _t->errorMessage(); break;
        case 30: *reinterpret_cast<bool*>(_v) = _t->busy(); break;
        case 31: *reinterpret_cast<QString*>(_v) = _t->serverUrl(); break;
        default: break;
        }
    }
    if (_c == QMetaObject::WriteProperty) {
        void *_v = _a[0];
        switch (_id) {
        case 7: _t->setSelectedAthleteId(*reinterpret_cast<QString*>(_v)); break;
        case 17: _t->setAnalyticsPeriod(*reinterpret_cast<QString*>(_v)); break;
        case 24: _t->setCreateDialogOpen(*reinterpret_cast<bool*>(_v)); break;
        case 26: _t->setViewMode(*reinterpret_cast<QString*>(_v)); break;
        case 31: _t->setServerUrl(*reinterpret_cast<QString*>(_v)); break;
        default: break;
        }
    }
}

const QMetaObject *WorkoutStore::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *WorkoutStore::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_staticMetaObjectStaticContent<qt_meta_tag_ZN12WorkoutStoreE_t>.strings))
        return static_cast<void*>(this);
    return QObject::qt_metacast(_clname);
}

int WorkoutStore::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 80)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 80;
    }
    if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 80)
            *reinterpret_cast<QMetaType *>(_a[0]) = QMetaType();
        _id -= 80;
    }
    if (_c == QMetaObject::ReadProperty || _c == QMetaObject::WriteProperty
            || _c == QMetaObject::ResetProperty || _c == QMetaObject::BindableProperty
            || _c == QMetaObject::RegisterPropertyMetaType) {
        qt_static_metacall(this, _c, _id, _a);
        _id -= 32;
    }
    return _id;
}

// SIGNAL 0
void WorkoutStore::loginStateChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 0, nullptr);
}

// SIGNAL 1
void WorkoutStore::loginSucceeded()
{
    QMetaObject::activate(this, &staticMetaObject, 1, nullptr);
}

// SIGNAL 2
void WorkoutStore::loginFailed(const QString & _t1)
{
    QMetaObject::activate<void>(this, &staticMetaObject, 2, nullptr, _t1);
}

// SIGNAL 3
void WorkoutStore::loggedOut()
{
    QMetaObject::activate(this, &staticMetaObject, 3, nullptr);
}

// SIGNAL 4
void WorkoutStore::sessionExpired()
{
    QMetaObject::activate(this, &staticMetaObject, 4, nullptr);
}

// SIGNAL 5
void WorkoutStore::authErrorChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 5, nullptr);
}

// SIGNAL 6
void WorkoutStore::athleteLinked(const QString & _t1)
{
    QMetaObject::activate<void>(this, &staticMetaObject, 6, nullptr, _t1);
}

// SIGNAL 7
void WorkoutStore::athleteLinkFailed(const QString & _t1)
{
    QMetaObject::activate<void>(this, &staticMetaObject, 7, nullptr, _t1);
}

// SIGNAL 8
void WorkoutStore::calendarChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 8, nullptr);
}

// SIGNAL 9
void WorkoutStore::athletesChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 9, nullptr);
}

// SIGNAL 10
void WorkoutStore::selectedAthleteChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 10, nullptr);
}

// SIGNAL 11
void WorkoutStore::selectedDateChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 11, nullptr);
}

// SIGNAL 12
void WorkoutStore::selectedDayChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 12, nullptr);
}

// SIGNAL 13
void WorkoutStore::selectedWorkoutChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 13, nullptr);
}

// SIGNAL 14
void WorkoutStore::selectedWorkoutCommentsChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 14, nullptr);
}

// SIGNAL 15
void WorkoutStore::analyticsChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 15, nullptr);
}

// SIGNAL 16
void WorkoutStore::aiCoachReportChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 16, nullptr);
}

// SIGNAL 17
void WorkoutStore::aiCoachPlanApplied(int _t1, int _t2)
{
    QMetaObject::activate<void>(this, &staticMetaObject, 17, nullptr, _t1, _t2);
}

// SIGNAL 18
void WorkoutStore::aiCoachChatReply(const QString & _t1)
{
    QMetaObject::activate<void>(this, &staticMetaObject, 18, nullptr, _t1);
}

// SIGNAL 19
void WorkoutStore::analyticsPeriodChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 19, nullptr);
}

// SIGNAL 20
void WorkoutStore::goalsChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 20, nullptr);
}

// SIGNAL 21
void WorkoutStore::routesChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 21, nullptr);
}

// SIGNAL 22
void WorkoutStore::openAiKeyChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 22, nullptr);
}

// SIGNAL 23
void WorkoutStore::stravaStatusChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 23, nullptr);
}

// SIGNAL 24
void WorkoutStore::stravaSyncDone(int _t1)
{
    QMetaObject::activate<void>(this, &staticMetaObject, 24, nullptr, _t1);
}

// SIGNAL 25
void WorkoutStore::serverUrlChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 25, nullptr);
}

// SIGNAL 26
void WorkoutStore::templatesChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 26, nullptr);
}

// SIGNAL 27
void WorkoutStore::createDialogOpenChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 27, nullptr);
}

// SIGNAL 28
void WorkoutStore::draftChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 28, nullptr);
}

// SIGNAL 29
void WorkoutStore::viewModeChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 29, nullptr);
}

// SIGNAL 30
void WorkoutStore::errorChanged(const QString & _t1)
{
    QMetaObject::activate<void>(this, &staticMetaObject, 30, nullptr, _t1);
}

// SIGNAL 31
void WorkoutStore::busyChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 31, nullptr);
}

// SIGNAL 32
void WorkoutStore::workoutCreated()
{
    QMetaObject::activate(this, &staticMetaObject, 32, nullptr);
}
QT_WARNING_POP
