#pragma once

#include <QObject>
#include <QDate>
#include <QVariantList>
#include <QVariantMap>
#include <QStringList>
#include <QSqlDatabase>

class WorkoutStore : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString monthLabel READ monthLabel NOTIFY calendarChanged)
    Q_PROPERTY(QVariantList users READ users NOTIFY usersChanged)
    Q_PROPERTY(QString currentUserId READ currentUserId WRITE setCurrentUserId NOTIFY currentUserChanged)
    Q_PROPERTY(QString currentUserRole READ currentUserRole NOTIFY currentUserChanged)
    Q_PROPERTY(bool canEditWorkouts READ canEditWorkouts NOTIFY currentUserChanged)
    Q_PROPERTY(QVariantList athletes READ athletes NOTIFY athletesChanged)
    Q_PROPERTY(QString selectedAthleteId READ selectedAthleteId WRITE setSelectedAthleteId NOTIFY selectedAthleteChanged)
    Q_PROPERTY(QString selectedAthleteName READ selectedAthleteName NOTIFY selectedAthleteChanged)
    Q_PROPERTY(QString selectedDateIso READ selectedDateIso NOTIFY selectedDateChanged)
    Q_PROPERTY(QString selectedDayLabel READ selectedDayLabel NOTIFY selectedDateChanged)
    Q_PROPERTY(QVariantList dayCells READ dayCells NOTIFY calendarChanged)
    Q_PROPERTY(QVariantList selectedDayWorkouts READ selectedDayWorkouts NOTIFY selectedDayChanged)
    Q_PROPERTY(QVariantMap selectedWorkout READ selectedWorkout NOTIFY selectedWorkoutChanged)
    Q_PROPERTY(QVariantList selectedWorkoutComments READ selectedWorkoutComments NOTIFY selectedWorkoutCommentsChanged)
    Q_PROPERTY(QVariantMap analyticsSummary READ analyticsSummary NOTIFY analyticsChanged)
    Q_PROPERTY(QVariantList templateLibrary READ templateLibrary NOTIFY templatesChanged)
    Q_PROPERTY(bool createDialogOpen READ createDialogOpen WRITE setCreateDialogOpen NOTIFY createDialogOpenChanged)
    Q_PROPERTY(QString draftDateIso READ draftDateIso NOTIFY draftChanged)
    Q_PROPERTY(QString viewMode READ viewMode WRITE setViewMode NOTIFY viewModeChanged)
    Q_PROPERTY(QStringList categories READ categories CONSTANT)
    Q_PROPERTY(QStringList intensities READ intensities CONSTANT)
    Q_PROPERTY(QString errorMessage READ errorMessage NOTIFY errorChanged)
    Q_PROPERTY(bool busy READ busy NOTIFY busyChanged)

public:
    explicit WorkoutStore(QObject *parent = nullptr);

    QString monthLabel() const;
    QVariantList users() const;
    QString currentUserId() const;
    void setCurrentUserId(const QString &userId);
    QString currentUserRole() const;
    bool canEditWorkouts() const;
    QVariantList athletes() const;
    QString selectedAthleteId() const;
    void setSelectedAthleteId(const QString &athleteId);
    QString selectedAthleteName() const;
    QString selectedDateIso() const;
    QString selectedDayLabel() const;
    QVariantList dayCells() const;
    QVariantList selectedDayWorkouts() const;
    QVariantMap selectedWorkout() const;
    QVariantList selectedWorkoutComments() const;
    QVariantMap analyticsSummary() const;
    QVariantList templateLibrary() const;

    bool createDialogOpen() const;
    void setCreateDialogOpen(bool open);
    QString draftDateIso() const;

    QString viewMode() const;
    void setViewMode(const QString &mode);
    QStringList categories() const;
    QStringList intensities() const;
    QString errorMessage() const;
    bool busy() const;

    Q_INVOKABLE void goToToday();
    Q_INVOKABLE void prevMonth();
    Q_INVOKABLE void nextMonth();
    Q_INVOKABLE void selectDate(const QString &dateIso);
    Q_INVOKABLE void openCreateDialogForDate(const QString &dateIso);
    Q_INVOKABLE void cancelCreateDialog();
    Q_INVOKABLE bool createWorkout(
        const QString &title,
        const QString &category,
        double distanceKm,
        int durationMin,
        const QString &intensity,
        const QString &notes,
        bool hiddenFromAthlete = false,
        const QString &intervalsJson = QString()
    );
    Q_INVOKABLE void selectWorkout(const QString &id);
    Q_INVOKABLE bool addComment(const QString &author, const QString &text);
    Q_INVOKABLE bool saveTemplate(
        const QString &title,
        const QString &category,
        double distanceKm,
        int durationMin,
        const QString &intensity,
        const QString &intervals,
        const QString &notes,
        const QString &tags
    );
    Q_INVOKABLE bool planFromTemplate(const QString &templateId, const QString &dateIso);
    Q_INVOKABLE bool updateWorkout(
        const QString &id,
        const QString &title,
        const QString &category,
        double distanceKm,
        int durationMin,
        const QString &intensity,
        const QString &notes,
        bool hiddenFromAthlete = false,
        const QString &intervalsJson = QString()
    );
    Q_INVOKABLE bool deleteWorkout(const QString &id);
    Q_INVOKABLE bool updateTemplate(
        const QString &id,
        const QString &title,
        const QString &category,
        double distanceKm,
        int durationMin,
        const QString &intensity,
        const QString &intervals,
        const QString &notes,
        const QString &tags
    );
    Q_INVOKABLE bool deleteTemplate(const QString &id);
    Q_INVOKABLE bool markWorkoutStatus(const QString &workoutId, const QString &status, const QString &feedback);
    Q_INVOKABLE bool markWorkoutStatusDetailed(
        const QString &workoutId,
        const QString &status,
        const QString &feedback,
        const QString &mood,
        int perceivedExertion
    );
    Q_INVOKABLE bool canCurrentUserEditAthlete(const QString &athleteId) const;
    Q_INVOKABLE void clearError();
    Q_INVOKABLE void refresh();

signals:
    void calendarChanged();
    void athletesChanged();
    void usersChanged();
    void currentUserChanged();
    void selectedAthleteChanged();
    void selectedDateChanged();
    void selectedDayChanged();
    void selectedWorkoutChanged();
    void selectedWorkoutCommentsChanged();
    void analyticsChanged();
    void templatesChanged();
    void createDialogOpenChanged();
    void draftChanged();
    void viewModeChanged();
    void errorChanged(const QString &message);
    void busyChanged();
    void workoutCreated();

private:
    bool initDatabase();
    void seedDatabase();
    bool ensureSchema();
    QString databasePath() const;
    QString generateId() const;
    QVariantMap workoutToCardMap(const QVariantMap &w) const;
    QVariantMap workoutToDetailMap(const QVariantMap &w) const;
    QString categoryIcon(const QString &category) const;
    QString categoryColor(const QString &category) const;
    QString intensityColor(const QString &intensity) const;
    QVariantList workoutsForDate(const QDate &date) const;
    QVariantMap workoutById(const QString &workoutId) const;
    QVariantList commentsForWorkout(const QString &workoutId) const;
    bool validateIntervalsJson(const QString &intervalsJson, QString *normalized) const;
    bool isCoach() const;
    bool isAthlete() const;
    bool hasAccessToAthlete(const QString &athleteId) const;
    bool hasWriteAccessToWorkout(const QString &workoutId) const;
    void setError(const QString &message);
    void setBusy(bool value);
    void emitDataChanged();

    QDate m_monthStart;
    QDate m_selectedDate;
    QDate m_draftDate;
    bool m_createDialogOpen = false;
    QString m_viewMode = QStringLiteral("month");
    QString m_selectedWorkoutId;
    QString m_selectedAthleteId;
    QString m_currentUserId;
    QString m_errorMessage;
    bool m_busy = false;
    QSqlDatabase m_db;
};

