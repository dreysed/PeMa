/****************************************************************************
** Meta object code from reading C++ file 'WorkoutStore.h'
**
** Created by: The Qt Meta Object Compiler version 69 (Qt 6.10.2)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "../../../src/backend/WorkoutStore.h"
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
        "calendarChanged",
        "",
        "athletesChanged",
        "usersChanged",
        "currentUserChanged",
        "selectedAthleteChanged",
        "selectedDateChanged",
        "selectedDayChanged",
        "selectedWorkoutChanged",
        "selectedWorkoutCommentsChanged",
        "analyticsChanged",
        "templatesChanged",
        "createDialogOpenChanged",
        "draftChanged",
        "viewModeChanged",
        "errorChanged",
        "message",
        "busyChanged",
        "workoutCreated",
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
        "selectWorkout",
        "id",
        "addComment",
        "author",
        "text",
        "saveTemplate",
        "intervals",
        "tags",
        "planFromTemplate",
        "templateId",
        "updateWorkout",
        "deleteWorkout",
        "updateTemplate",
        "deleteTemplate",
        "markWorkoutStatus",
        "workoutId",
        "status",
        "feedback",
        "markWorkoutStatusDetailed",
        "mood",
        "perceivedExertion",
        "canCurrentUserEditAthlete",
        "athleteId",
        "clearError",
        "refresh",
        "monthLabel",
        "users",
        "QVariantList",
        "currentUserId",
        "currentUserRole",
        "canEditWorkouts",
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
        "templateLibrary",
        "createDialogOpen",
        "draftDateIso",
        "viewMode",
        "categories",
        "intensities",
        "errorMessage",
        "busy"
    };

    QtMocHelpers::UintData qt_methods {
        // Signal 'calendarChanged'
        QtMocHelpers::SignalData<void()>(1, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'athletesChanged'
        QtMocHelpers::SignalData<void()>(3, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'usersChanged'
        QtMocHelpers::SignalData<void()>(4, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'currentUserChanged'
        QtMocHelpers::SignalData<void()>(5, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'selectedAthleteChanged'
        QtMocHelpers::SignalData<void()>(6, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'selectedDateChanged'
        QtMocHelpers::SignalData<void()>(7, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'selectedDayChanged'
        QtMocHelpers::SignalData<void()>(8, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'selectedWorkoutChanged'
        QtMocHelpers::SignalData<void()>(9, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'selectedWorkoutCommentsChanged'
        QtMocHelpers::SignalData<void()>(10, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'analyticsChanged'
        QtMocHelpers::SignalData<void()>(11, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'templatesChanged'
        QtMocHelpers::SignalData<void()>(12, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'createDialogOpenChanged'
        QtMocHelpers::SignalData<void()>(13, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'draftChanged'
        QtMocHelpers::SignalData<void()>(14, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'viewModeChanged'
        QtMocHelpers::SignalData<void()>(15, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'errorChanged'
        QtMocHelpers::SignalData<void(const QString &)>(16, 2, QMC::AccessPublic, QMetaType::Void, {{
            { QMetaType::QString, 17 },
        }}),
        // Signal 'busyChanged'
        QtMocHelpers::SignalData<void()>(18, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'workoutCreated'
        QtMocHelpers::SignalData<void()>(19, 2, QMC::AccessPublic, QMetaType::Void),
        // Method 'goToToday'
        QtMocHelpers::MethodData<void()>(20, 2, QMC::AccessPublic, QMetaType::Void),
        // Method 'prevMonth'
        QtMocHelpers::MethodData<void()>(21, 2, QMC::AccessPublic, QMetaType::Void),
        // Method 'nextMonth'
        QtMocHelpers::MethodData<void()>(22, 2, QMC::AccessPublic, QMetaType::Void),
        // Method 'selectDate'
        QtMocHelpers::MethodData<void(const QString &)>(23, 2, QMC::AccessPublic, QMetaType::Void, {{
            { QMetaType::QString, 24 },
        }}),
        // Method 'openCreateDialogForDate'
        QtMocHelpers::MethodData<void(const QString &)>(25, 2, QMC::AccessPublic, QMetaType::Void, {{
            { QMetaType::QString, 24 },
        }}),
        // Method 'cancelCreateDialog'
        QtMocHelpers::MethodData<void()>(26, 2, QMC::AccessPublic, QMetaType::Void),
        // Method 'createWorkout'
        QtMocHelpers::MethodData<bool(const QString &, const QString &, double, int, const QString &, const QString &, bool, const QString &)>(27, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { QMetaType::QString, 28 }, { QMetaType::QString, 29 }, { QMetaType::Double, 30 }, { QMetaType::Int, 31 },
            { QMetaType::QString, 32 }, { QMetaType::QString, 33 }, { QMetaType::Bool, 34 }, { QMetaType::QString, 35 },
        }}),
        // Method 'createWorkout'
        QtMocHelpers::MethodData<bool(const QString &, const QString &, double, int, const QString &, const QString &, bool)>(27, 2, QMC::AccessPublic | QMC::MethodCloned, QMetaType::Bool, {{
            { QMetaType::QString, 28 }, { QMetaType::QString, 29 }, { QMetaType::Double, 30 }, { QMetaType::Int, 31 },
            { QMetaType::QString, 32 }, { QMetaType::QString, 33 }, { QMetaType::Bool, 34 },
        }}),
        // Method 'createWorkout'
        QtMocHelpers::MethodData<bool(const QString &, const QString &, double, int, const QString &, const QString &)>(27, 2, QMC::AccessPublic | QMC::MethodCloned, QMetaType::Bool, {{
            { QMetaType::QString, 28 }, { QMetaType::QString, 29 }, { QMetaType::Double, 30 }, { QMetaType::Int, 31 },
            { QMetaType::QString, 32 }, { QMetaType::QString, 33 },
        }}),
        // Method 'selectWorkout'
        QtMocHelpers::MethodData<void(const QString &)>(36, 2, QMC::AccessPublic, QMetaType::Void, {{
            { QMetaType::QString, 37 },
        }}),
        // Method 'addComment'
        QtMocHelpers::MethodData<bool(const QString &, const QString &)>(38, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { QMetaType::QString, 39 }, { QMetaType::QString, 40 },
        }}),
        // Method 'saveTemplate'
        QtMocHelpers::MethodData<bool(const QString &, const QString &, double, int, const QString &, const QString &, const QString &, const QString &)>(41, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { QMetaType::QString, 28 }, { QMetaType::QString, 29 }, { QMetaType::Double, 30 }, { QMetaType::Int, 31 },
            { QMetaType::QString, 32 }, { QMetaType::QString, 42 }, { QMetaType::QString, 33 }, { QMetaType::QString, 43 },
        }}),
        // Method 'planFromTemplate'
        QtMocHelpers::MethodData<bool(const QString &, const QString &)>(44, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { QMetaType::QString, 45 }, { QMetaType::QString, 24 },
        }}),
        // Method 'updateWorkout'
        QtMocHelpers::MethodData<bool(const QString &, const QString &, const QString &, double, int, const QString &, const QString &, bool, const QString &)>(46, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { QMetaType::QString, 37 }, { QMetaType::QString, 28 }, { QMetaType::QString, 29 }, { QMetaType::Double, 30 },
            { QMetaType::Int, 31 }, { QMetaType::QString, 32 }, { QMetaType::QString, 33 }, { QMetaType::Bool, 34 },
            { QMetaType::QString, 35 },
        }}),
        // Method 'updateWorkout'
        QtMocHelpers::MethodData<bool(const QString &, const QString &, const QString &, double, int, const QString &, const QString &, bool)>(46, 2, QMC::AccessPublic | QMC::MethodCloned, QMetaType::Bool, {{
            { QMetaType::QString, 37 }, { QMetaType::QString, 28 }, { QMetaType::QString, 29 }, { QMetaType::Double, 30 },
            { QMetaType::Int, 31 }, { QMetaType::QString, 32 }, { QMetaType::QString, 33 }, { QMetaType::Bool, 34 },
        }}),
        // Method 'updateWorkout'
        QtMocHelpers::MethodData<bool(const QString &, const QString &, const QString &, double, int, const QString &, const QString &)>(46, 2, QMC::AccessPublic | QMC::MethodCloned, QMetaType::Bool, {{
            { QMetaType::QString, 37 }, { QMetaType::QString, 28 }, { QMetaType::QString, 29 }, { QMetaType::Double, 30 },
            { QMetaType::Int, 31 }, { QMetaType::QString, 32 }, { QMetaType::QString, 33 },
        }}),
        // Method 'deleteWorkout'
        QtMocHelpers::MethodData<bool(const QString &)>(47, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { QMetaType::QString, 37 },
        }}),
        // Method 'updateTemplate'
        QtMocHelpers::MethodData<bool(const QString &, const QString &, const QString &, double, int, const QString &, const QString &, const QString &, const QString &)>(48, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { QMetaType::QString, 37 }, { QMetaType::QString, 28 }, { QMetaType::QString, 29 }, { QMetaType::Double, 30 },
            { QMetaType::Int, 31 }, { QMetaType::QString, 32 }, { QMetaType::QString, 42 }, { QMetaType::QString, 33 },
            { QMetaType::QString, 43 },
        }}),
        // Method 'deleteTemplate'
        QtMocHelpers::MethodData<bool(const QString &)>(49, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { QMetaType::QString, 37 },
        }}),
        // Method 'markWorkoutStatus'
        QtMocHelpers::MethodData<bool(const QString &, const QString &, const QString &)>(50, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { QMetaType::QString, 51 }, { QMetaType::QString, 52 }, { QMetaType::QString, 53 },
        }}),
        // Method 'markWorkoutStatusDetailed'
        QtMocHelpers::MethodData<bool(const QString &, const QString &, const QString &, const QString &, int)>(54, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { QMetaType::QString, 51 }, { QMetaType::QString, 52 }, { QMetaType::QString, 53 }, { QMetaType::QString, 55 },
            { QMetaType::Int, 56 },
        }}),
        // Method 'canCurrentUserEditAthlete'
        QtMocHelpers::MethodData<bool(const QString &) const>(57, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { QMetaType::QString, 58 },
        }}),
        // Method 'clearError'
        QtMocHelpers::MethodData<void()>(59, 2, QMC::AccessPublic, QMetaType::Void),
        // Method 'refresh'
        QtMocHelpers::MethodData<void()>(60, 2, QMC::AccessPublic, QMetaType::Void),
    };
    QtMocHelpers::UintData qt_properties {
        // property 'monthLabel'
        QtMocHelpers::PropertyData<QString>(61, QMetaType::QString, QMC::DefaultPropertyFlags, 0),
        // property 'users'
        QtMocHelpers::PropertyData<QVariantList>(62, 0x80000000 | 63, QMC::DefaultPropertyFlags | QMC::EnumOrFlag, 2),
        // property 'currentUserId'
        QtMocHelpers::PropertyData<QString>(64, QMetaType::QString, QMC::DefaultPropertyFlags | QMC::Writable | QMC::StdCppSet, 3),
        // property 'currentUserRole'
        QtMocHelpers::PropertyData<QString>(65, QMetaType::QString, QMC::DefaultPropertyFlags, 3),
        // property 'canEditWorkouts'
        QtMocHelpers::PropertyData<bool>(66, QMetaType::Bool, QMC::DefaultPropertyFlags, 3),
        // property 'athletes'
        QtMocHelpers::PropertyData<QVariantList>(67, 0x80000000 | 63, QMC::DefaultPropertyFlags | QMC::EnumOrFlag, 1),
        // property 'selectedAthleteId'
        QtMocHelpers::PropertyData<QString>(68, QMetaType::QString, QMC::DefaultPropertyFlags | QMC::Writable | QMC::StdCppSet, 4),
        // property 'selectedAthleteName'
        QtMocHelpers::PropertyData<QString>(69, QMetaType::QString, QMC::DefaultPropertyFlags, 4),
        // property 'selectedDateIso'
        QtMocHelpers::PropertyData<QString>(70, QMetaType::QString, QMC::DefaultPropertyFlags, 5),
        // property 'selectedDayLabel'
        QtMocHelpers::PropertyData<QString>(71, QMetaType::QString, QMC::DefaultPropertyFlags, 5),
        // property 'dayCells'
        QtMocHelpers::PropertyData<QVariantList>(72, 0x80000000 | 63, QMC::DefaultPropertyFlags | QMC::EnumOrFlag, 0),
        // property 'selectedDayWorkouts'
        QtMocHelpers::PropertyData<QVariantList>(73, 0x80000000 | 63, QMC::DefaultPropertyFlags | QMC::EnumOrFlag, 6),
        // property 'selectedWorkout'
        QtMocHelpers::PropertyData<QVariantMap>(74, 0x80000000 | 75, QMC::DefaultPropertyFlags | QMC::EnumOrFlag, 7),
        // property 'selectedWorkoutComments'
        QtMocHelpers::PropertyData<QVariantList>(76, 0x80000000 | 63, QMC::DefaultPropertyFlags | QMC::EnumOrFlag, 8),
        // property 'analyticsSummary'
        QtMocHelpers::PropertyData<QVariantMap>(77, 0x80000000 | 75, QMC::DefaultPropertyFlags | QMC::EnumOrFlag, 9),
        // property 'templateLibrary'
        QtMocHelpers::PropertyData<QVariantList>(78, 0x80000000 | 63, QMC::DefaultPropertyFlags | QMC::EnumOrFlag, 10),
        // property 'createDialogOpen'
        QtMocHelpers::PropertyData<bool>(79, QMetaType::Bool, QMC::DefaultPropertyFlags | QMC::Writable | QMC::StdCppSet, 11),
        // property 'draftDateIso'
        QtMocHelpers::PropertyData<QString>(80, QMetaType::QString, QMC::DefaultPropertyFlags, 12),
        // property 'viewMode'
        QtMocHelpers::PropertyData<QString>(81, QMetaType::QString, QMC::DefaultPropertyFlags | QMC::Writable | QMC::StdCppSet, 13),
        // property 'categories'
        QtMocHelpers::PropertyData<QStringList>(82, QMetaType::QStringList, QMC::DefaultPropertyFlags | QMC::Constant),
        // property 'intensities'
        QtMocHelpers::PropertyData<QStringList>(83, QMetaType::QStringList, QMC::DefaultPropertyFlags | QMC::Constant),
        // property 'errorMessage'
        QtMocHelpers::PropertyData<QString>(84, QMetaType::QString, QMC::DefaultPropertyFlags, 14),
        // property 'busy'
        QtMocHelpers::PropertyData<bool>(85, QMetaType::Bool, QMC::DefaultPropertyFlags, 15),
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
        case 0: _t->calendarChanged(); break;
        case 1: _t->athletesChanged(); break;
        case 2: _t->usersChanged(); break;
        case 3: _t->currentUserChanged(); break;
        case 4: _t->selectedAthleteChanged(); break;
        case 5: _t->selectedDateChanged(); break;
        case 6: _t->selectedDayChanged(); break;
        case 7: _t->selectedWorkoutChanged(); break;
        case 8: _t->selectedWorkoutCommentsChanged(); break;
        case 9: _t->analyticsChanged(); break;
        case 10: _t->templatesChanged(); break;
        case 11: _t->createDialogOpenChanged(); break;
        case 12: _t->draftChanged(); break;
        case 13: _t->viewModeChanged(); break;
        case 14: _t->errorChanged((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1]))); break;
        case 15: _t->busyChanged(); break;
        case 16: _t->workoutCreated(); break;
        case 17: _t->goToToday(); break;
        case 18: _t->prevMonth(); break;
        case 19: _t->nextMonth(); break;
        case 20: _t->selectDate((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1]))); break;
        case 21: _t->openCreateDialogForDate((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1]))); break;
        case 22: _t->cancelCreateDialog(); break;
        case 23: { bool _r = _t->createWorkout((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[2])),(*reinterpret_cast<std::add_pointer_t<double>>(_a[3])),(*reinterpret_cast<std::add_pointer_t<int>>(_a[4])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[5])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[6])),(*reinterpret_cast<std::add_pointer_t<bool>>(_a[7])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[8])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 24: { bool _r = _t->createWorkout((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[2])),(*reinterpret_cast<std::add_pointer_t<double>>(_a[3])),(*reinterpret_cast<std::add_pointer_t<int>>(_a[4])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[5])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[6])),(*reinterpret_cast<std::add_pointer_t<bool>>(_a[7])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 25: { bool _r = _t->createWorkout((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[2])),(*reinterpret_cast<std::add_pointer_t<double>>(_a[3])),(*reinterpret_cast<std::add_pointer_t<int>>(_a[4])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[5])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[6])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 26: _t->selectWorkout((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1]))); break;
        case 27: { bool _r = _t->addComment((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[2])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 28: { bool _r = _t->saveTemplate((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[2])),(*reinterpret_cast<std::add_pointer_t<double>>(_a[3])),(*reinterpret_cast<std::add_pointer_t<int>>(_a[4])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[5])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[6])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[7])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[8])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 29: { bool _r = _t->planFromTemplate((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[2])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 30: { bool _r = _t->updateWorkout((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[2])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[3])),(*reinterpret_cast<std::add_pointer_t<double>>(_a[4])),(*reinterpret_cast<std::add_pointer_t<int>>(_a[5])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[6])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[7])),(*reinterpret_cast<std::add_pointer_t<bool>>(_a[8])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[9])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 31: { bool _r = _t->updateWorkout((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[2])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[3])),(*reinterpret_cast<std::add_pointer_t<double>>(_a[4])),(*reinterpret_cast<std::add_pointer_t<int>>(_a[5])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[6])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[7])),(*reinterpret_cast<std::add_pointer_t<bool>>(_a[8])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 32: { bool _r = _t->updateWorkout((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[2])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[3])),(*reinterpret_cast<std::add_pointer_t<double>>(_a[4])),(*reinterpret_cast<std::add_pointer_t<int>>(_a[5])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[6])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[7])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 33: { bool _r = _t->deleteWorkout((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 34: { bool _r = _t->updateTemplate((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[2])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[3])),(*reinterpret_cast<std::add_pointer_t<double>>(_a[4])),(*reinterpret_cast<std::add_pointer_t<int>>(_a[5])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[6])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[7])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[8])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[9])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 35: { bool _r = _t->deleteTemplate((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 36: { bool _r = _t->markWorkoutStatus((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[2])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[3])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 37: { bool _r = _t->markWorkoutStatusDetailed((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[2])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[3])),(*reinterpret_cast<std::add_pointer_t<QString>>(_a[4])),(*reinterpret_cast<std::add_pointer_t<int>>(_a[5])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 38: { bool _r = _t->canCurrentUserEditAthlete((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1])));
            if (_a[0]) *reinterpret_cast<bool*>(_a[0]) = std::move(_r); }  break;
        case 39: _t->clearError(); break;
        case 40: _t->refresh(); break;
        default: ;
        }
    }
    if (_c == QMetaObject::IndexOfMethod) {
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::calendarChanged, 0))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::athletesChanged, 1))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::usersChanged, 2))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::currentUserChanged, 3))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::selectedAthleteChanged, 4))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::selectedDateChanged, 5))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::selectedDayChanged, 6))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::selectedWorkoutChanged, 7))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::selectedWorkoutCommentsChanged, 8))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::analyticsChanged, 9))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::templatesChanged, 10))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::createDialogOpenChanged, 11))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::draftChanged, 12))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::viewModeChanged, 13))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)(const QString & )>(_a, &WorkoutStore::errorChanged, 14))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::busyChanged, 15))
            return;
        if (QtMocHelpers::indexOfMethod<void (WorkoutStore::*)()>(_a, &WorkoutStore::workoutCreated, 16))
            return;
    }
    if (_c == QMetaObject::ReadProperty) {
        void *_v = _a[0];
        switch (_id) {
        case 0: *reinterpret_cast<QString*>(_v) = _t->monthLabel(); break;
        case 1: *reinterpret_cast<QVariantList*>(_v) = _t->users(); break;
        case 2: *reinterpret_cast<QString*>(_v) = _t->currentUserId(); break;
        case 3: *reinterpret_cast<QString*>(_v) = _t->currentUserRole(); break;
        case 4: *reinterpret_cast<bool*>(_v) = _t->canEditWorkouts(); break;
        case 5: *reinterpret_cast<QVariantList*>(_v) = _t->athletes(); break;
        case 6: *reinterpret_cast<QString*>(_v) = _t->selectedAthleteId(); break;
        case 7: *reinterpret_cast<QString*>(_v) = _t->selectedAthleteName(); break;
        case 8: *reinterpret_cast<QString*>(_v) = _t->selectedDateIso(); break;
        case 9: *reinterpret_cast<QString*>(_v) = _t->selectedDayLabel(); break;
        case 10: *reinterpret_cast<QVariantList*>(_v) = _t->dayCells(); break;
        case 11: *reinterpret_cast<QVariantList*>(_v) = _t->selectedDayWorkouts(); break;
        case 12: *reinterpret_cast<QVariantMap*>(_v) = _t->selectedWorkout(); break;
        case 13: *reinterpret_cast<QVariantList*>(_v) = _t->selectedWorkoutComments(); break;
        case 14: *reinterpret_cast<QVariantMap*>(_v) = _t->analyticsSummary(); break;
        case 15: *reinterpret_cast<QVariantList*>(_v) = _t->templateLibrary(); break;
        case 16: *reinterpret_cast<bool*>(_v) = _t->createDialogOpen(); break;
        case 17: *reinterpret_cast<QString*>(_v) = _t->draftDateIso(); break;
        case 18: *reinterpret_cast<QString*>(_v) = _t->viewMode(); break;
        case 19: *reinterpret_cast<QStringList*>(_v) = _t->categories(); break;
        case 20: *reinterpret_cast<QStringList*>(_v) = _t->intensities(); break;
        case 21: *reinterpret_cast<QString*>(_v) = _t->errorMessage(); break;
        case 22: *reinterpret_cast<bool*>(_v) = _t->busy(); break;
        default: break;
        }
    }
    if (_c == QMetaObject::WriteProperty) {
        void *_v = _a[0];
        switch (_id) {
        case 2: _t->setCurrentUserId(*reinterpret_cast<QString*>(_v)); break;
        case 6: _t->setSelectedAthleteId(*reinterpret_cast<QString*>(_v)); break;
        case 16: _t->setCreateDialogOpen(*reinterpret_cast<bool*>(_v)); break;
        case 18: _t->setViewMode(*reinterpret_cast<QString*>(_v)); break;
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
        if (_id < 41)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 41;
    }
    if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 41)
            *reinterpret_cast<QMetaType *>(_a[0]) = QMetaType();
        _id -= 41;
    }
    if (_c == QMetaObject::ReadProperty || _c == QMetaObject::WriteProperty
            || _c == QMetaObject::ResetProperty || _c == QMetaObject::BindableProperty
            || _c == QMetaObject::RegisterPropertyMetaType) {
        qt_static_metacall(this, _c, _id, _a);
        _id -= 23;
    }
    return _id;
}

// SIGNAL 0
void WorkoutStore::calendarChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 0, nullptr);
}

// SIGNAL 1
void WorkoutStore::athletesChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 1, nullptr);
}

// SIGNAL 2
void WorkoutStore::usersChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 2, nullptr);
}

// SIGNAL 3
void WorkoutStore::currentUserChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 3, nullptr);
}

// SIGNAL 4
void WorkoutStore::selectedAthleteChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 4, nullptr);
}

// SIGNAL 5
void WorkoutStore::selectedDateChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 5, nullptr);
}

// SIGNAL 6
void WorkoutStore::selectedDayChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 6, nullptr);
}

// SIGNAL 7
void WorkoutStore::selectedWorkoutChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 7, nullptr);
}

// SIGNAL 8
void WorkoutStore::selectedWorkoutCommentsChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 8, nullptr);
}

// SIGNAL 9
void WorkoutStore::analyticsChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 9, nullptr);
}

// SIGNAL 10
void WorkoutStore::templatesChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 10, nullptr);
}

// SIGNAL 11
void WorkoutStore::createDialogOpenChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 11, nullptr);
}

// SIGNAL 12
void WorkoutStore::draftChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 12, nullptr);
}

// SIGNAL 13
void WorkoutStore::viewModeChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 13, nullptr);
}

// SIGNAL 14
void WorkoutStore::errorChanged(const QString & _t1)
{
    QMetaObject::activate<void>(this, &staticMetaObject, 14, nullptr, _t1);
}

// SIGNAL 15
void WorkoutStore::busyChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 15, nullptr);
}

// SIGNAL 16
void WorkoutStore::workoutCreated()
{
    QMetaObject::activate(this, &staticMetaObject, 16, nullptr);
}
QT_WARNING_POP
