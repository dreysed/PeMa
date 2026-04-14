#include "backend/WorkoutStore.h"

#include <QDateTime>
#include <QDir>
#include <QFileInfo>
#include <QJsonParseError>
#include <QLocale>
#include <QStandardPaths>
#include <QSqlQuery>
#include <QSqlError>
#include <QJsonDocument>
#include <QJsonArray>
#include <QJsonObject>
#include <QRandomGenerator>
#include <QtMath>

WorkoutStore::WorkoutStore(QObject *parent)
    : QObject(parent)
{
    m_selectedDate = QDate::currentDate();
    m_monthStart = QDate(m_selectedDate.year(), m_selectedDate.month(), 1);
    m_draftDate = m_selectedDate;
    if (initDatabase())
        seedDatabase();
}

QString WorkoutStore::monthLabel() const
{
    return QLocale(QLocale::Russian).toString(m_monthStart, QStringLiteral("MMMM yyyy 'года'"));
}

QVariantList WorkoutStore::users() const
{
    QVariantList list;
    QSqlQuery q(m_db);
    q.prepare(QStringLiteral("SELECT id, name, role FROM users ORDER BY name"));
    if (!q.exec())
        return list;
    while (q.next()) {
        QVariantMap user;
        user.insert(QStringLiteral("id"), q.value(0).toString());
        user.insert(QStringLiteral("name"), q.value(1).toString());
        user.insert(QStringLiteral("role"), q.value(2).toString());
        list.push_back(user);
    }
    return list;
}

QString WorkoutStore::currentUserId() const
{
    return m_currentUserId;
}

void WorkoutStore::setCurrentUserId(const QString &userId)
{
    if (userId.trimmed().isEmpty() || userId == m_currentUserId)
        return;
    QSqlQuery q(m_db);
    q.prepare(QStringLiteral("SELECT COUNT(*) FROM users WHERE id = ?"));
    q.addBindValue(userId);
    if (!q.exec() || !q.next() || q.value(0).toInt() == 0) {
        setError(QStringLiteral("Пользователь не найден."));
        return;
    }
    m_currentUserId = userId;
    m_selectedWorkoutId.clear();

    const QVariantList availableAthletes = athletes();
    if (availableAthletes.isEmpty()) {
        m_selectedAthleteId.clear();
    } else if (!hasAccessToAthlete(m_selectedAthleteId)) {
        m_selectedAthleteId = availableAthletes.first().toMap().value(QStringLiteral("id")).toString();
    }

    emit currentUserChanged();
    emit selectedAthleteChanged();
    emitDataChanged();
}

QString WorkoutStore::currentUserRole() const
{
    if (m_currentUserId.isEmpty())
        return QStringLiteral("guest");
    QSqlQuery q(m_db);
    q.prepare(QStringLiteral("SELECT role FROM users WHERE id = ?"));
    q.addBindValue(m_currentUserId);
    if (!q.exec() || !q.next())
        return QStringLiteral("guest");
    return q.value(0).toString();
}

bool WorkoutStore::canEditWorkouts() const
{
    return isCoach();
}

QVariantList WorkoutStore::athletes() const
{
    QVariantList list;
    QSqlQuery q(m_db);
    if (isCoach()) {
        q.prepare(QStringLiteral(
            "SELECT a.id, a.name "
            "FROM athletes a "
            "JOIN coach_athlete_links l ON l.athleteId = a.id "
            "WHERE l.coachUserId = ? "
            "ORDER BY a.name"));
        q.addBindValue(m_currentUserId);
    } else {
        q.prepare(QStringLiteral(
            "SELECT a.id, a.name "
            "FROM athletes a "
            "JOIN users u ON u.athleteId = a.id "
            "WHERE u.id = ? "
            "ORDER BY a.name"));
        q.addBindValue(m_currentUserId);
    }
    if (!q.exec())
        return list;
    while (q.next()) {
        QVariantMap m;
        m.insert(QStringLiteral("id"), q.value(0).toString());
        m.insert(QStringLiteral("name"), q.value(1).toString());
        list.push_back(m);
    }
    return list;
}

QString WorkoutStore::selectedAthleteId() const
{
    return m_selectedAthleteId;
}

void WorkoutStore::setSelectedAthleteId(const QString &athleteId)
{
    if (m_selectedAthleteId == athleteId)
        return;
    if (athleteId.isEmpty() || !hasAccessToAthlete(athleteId)) {
        setError(QStringLiteral("Нет доступа к выбранному атлету."));
        return;
    }
    m_selectedAthleteId = athleteId;
    m_selectedWorkoutId.clear();
    emit selectedAthleteChanged();
    emitDataChanged();
}

QString WorkoutStore::selectedAthleteName() const
{
    QSqlQuery q(m_db);
    q.prepare(QStringLiteral("SELECT name FROM athletes WHERE id = ?"));
    q.addBindValue(m_selectedAthleteId);
    if (!q.exec() || !q.next())
        return QStringLiteral("Не выбран");
    return q.value(0).toString();
}

QString WorkoutStore::selectedDateIso() const
{
    return m_selectedDate.toString(Qt::ISODate);
}

QString WorkoutStore::selectedDayLabel() const
{
    return QLocale(QLocale::Russian).toString(m_selectedDate, QStringLiteral("d MMMM yyyy"));
}

QVariantList WorkoutStore::dayCells() const
{
    QVariantList cells;
    const QDate firstOfMonth(m_monthStart.year(), m_monthStart.month(), 1);
    const int mondayBased = (firstOfMonth.dayOfWeek() + 6) % 7; // Monday=0
    const QDate gridStart = firstOfMonth.addDays(-mondayBased);

    for (int i = 0; i < 42; ++i) {
        const QDate d = gridStart.addDays(i);
        const bool inCurrentMonth = d.month() == m_monthStart.month();
        const bool isSelected = d == m_selectedDate;
        const bool isToday = d == QDate::currentDate();
        const QVariantList dayWorkouts = workoutsForDate(d);

        QVariantList cards;
        for (int k = 0; k < dayWorkouts.size() && k < 3; ++k) {
            cards.push_back(workoutToCardMap(dayWorkouts[k].toMap()));
        }

        QString bg = QStringLiteral("#ffffff");
        if (isSelected) {
            bg = QStringLiteral("#f7dde4");
        } else if (!dayWorkouts.isEmpty()) {
            bg = QStringLiteral("#f4f6f8");
        } else if (!inCurrentMonth) {
            bg = QStringLiteral("#fafafa");
        }

        QVariantMap cell;
        cell.insert(QStringLiteral("dateIso"), d.toString(Qt::ISODate));
        cell.insert(QStringLiteral("dayNumber"), d.day());
        cell.insert(QStringLiteral("inCurrentMonth"), inCurrentMonth);
        cell.insert(QStringLiteral("isSelected"), isSelected);
        cell.insert(QStringLiteral("isToday"), isToday);
        cell.insert(QStringLiteral("background"), bg);
        cell.insert(QStringLiteral("workouts"), cards);
        cells.push_back(cell);
    }

    return cells;
}

QVariantList WorkoutStore::selectedDayWorkouts() const
{
    QVariantList out;
    const QVariantList list = workoutsForDate(m_selectedDate);
    for (const QVariant &v : list) {
        out.push_back(workoutToCardMap(v.toMap()));
    }
    return out;
}

QVariantMap WorkoutStore::selectedWorkout() const
{
    const QVariantList list = workoutsForDate(m_selectedDate);
    for (const QVariant &v : list) {
        const QVariantMap w = v.toMap();
        if (w.value(QStringLiteral("id")).toString() == m_selectedWorkoutId)
            return workoutToDetailMap(w);
    }
    if (!list.isEmpty())
        return workoutToDetailMap(list.first().toMap());
    return {};
}

QVariantList WorkoutStore::selectedWorkoutComments() const
{
    if (m_selectedWorkoutId.isEmpty())
        return {};
    return commentsForWorkout(m_selectedWorkoutId);
}

QVariantMap WorkoutStore::analyticsSummary() const
{
    QVariantMap m;
    QSqlQuery q(m_db);
    q.prepare(QStringLiteral(
        "SELECT COUNT(*), COALESCE(SUM(durationMin),0), COALESCE(SUM(distanceKm),0) "
        "FROM workouts WHERE athleteId = ?"));
    q.addBindValue(m_selectedAthleteId);
    if (q.exec() && q.next()) {
        m.insert(QStringLiteral("workoutsCount"), q.value(0).toInt());
        m.insert(QStringLiteral("durationTotal"), q.value(1).toInt());
        m.insert(QStringLiteral("distanceTotal"), q.value(2).toDouble());
    } else {
        m.insert(QStringLiteral("workoutsCount"), 0);
        m.insert(QStringLiteral("durationTotal"), 0);
        m.insert(QStringLiteral("distanceTotal"), 0.0);
    }

    q.prepare(QStringLiteral(
        "SELECT intensity, COUNT(*) FROM workouts WHERE athleteId = ? GROUP BY intensity"));
    q.addBindValue(m_selectedAthleteId);
    QVariantMap byIntensity;
    if (q.exec()) {
        while (q.next()) {
            byIntensity.insert(q.value(0).toString(), q.value(1).toInt());
        }
    }
    m.insert(QStringLiteral("byIntensity"), byIntensity);
    return m;
}

QVariantList WorkoutStore::templateLibrary() const
{
    QVariantList list;
    QSqlQuery q(m_db);
    q.prepare(QStringLiteral(
        "SELECT id, title, category, distanceKm, durationMin, intensity, intervalsJson, notes, tags "
        "FROM templates ORDER BY title"));
    if (!q.exec())
        return list;
    while (q.next()) {
        QVariantMap t;
        t.insert(QStringLiteral("id"), q.value(0).toString());
        t.insert(QStringLiteral("title"), q.value(1).toString());
        t.insert(QStringLiteral("category"), q.value(2).toString());
        t.insert(QStringLiteral("distanceKm"), q.value(3).toDouble());
        t.insert(QStringLiteral("durationMin"), q.value(4).toInt());
        t.insert(QStringLiteral("intensity"), q.value(5).toString());
        t.insert(QStringLiteral("intervals"), q.value(6).toString());
        t.insert(QStringLiteral("notes"), q.value(7).toString());
        t.insert(QStringLiteral("tags"), q.value(8).toString());
        list.push_back(t);
    }
    return list;
}

bool WorkoutStore::createDialogOpen() const
{
    return m_createDialogOpen;
}

void WorkoutStore::setCreateDialogOpen(bool open)
{
    if (m_createDialogOpen == open)
        return;
    m_createDialogOpen = open;
    emit createDialogOpenChanged();
}

QString WorkoutStore::draftDateIso() const
{
    return m_draftDate.toString(Qt::ISODate);
}

QString WorkoutStore::viewMode() const
{
    return m_viewMode;
}

void WorkoutStore::setViewMode(const QString &mode)
{
    if (m_viewMode == mode)
        return;
    m_viewMode = mode;
    emit viewModeChanged();
}

QStringList WorkoutStore::categories() const
{
    return {QStringLiteral("run"), QStringLiteral("bike"), QStringLiteral("swim")};
}

QStringList WorkoutStore::intensities() const
{
    return {QStringLiteral("easy"), QStringLiteral("moderate"), QStringLiteral("hard")};
}

QString WorkoutStore::errorMessage() const
{
    return m_errorMessage;
}

bool WorkoutStore::busy() const
{
    return m_busy;
}

void WorkoutStore::goToToday()
{
    m_selectedDate = QDate::currentDate();
    m_monthStart = QDate(m_selectedDate.year(), m_selectedDate.month(), 1);
    emit selectedDateChanged();
    emit selectedDayChanged();
    emit calendarChanged();
    emitDataChanged();
}

void WorkoutStore::prevMonth()
{
    m_monthStart = m_monthStart.addMonths(-1);
    emit calendarChanged();
}

void WorkoutStore::nextMonth()
{
    m_monthStart = m_monthStart.addMonths(1);
    emit calendarChanged();
}

void WorkoutStore::selectDate(const QString &dateIso)
{
    const QDate d = QDate::fromString(dateIso, Qt::ISODate);
    if (!d.isValid() || d == m_selectedDate)
        return;
    m_selectedDate = d;
    emit selectedDateChanged();
    emit selectedDayChanged();
    emit calendarChanged();
    emit selectedWorkoutChanged();
    emit selectedWorkoutCommentsChanged();
}

void WorkoutStore::openCreateDialogForDate(const QString &dateIso)
{
    const QDate d = QDate::fromString(dateIso, Qt::ISODate);
    if (!d.isValid())
        return;
    m_draftDate = d;
    emit draftChanged();
    setCreateDialogOpen(true);
}

void WorkoutStore::cancelCreateDialog()
{
    setCreateDialogOpen(false);
}

bool WorkoutStore::createWorkout(
    const QString &title,
    const QString &category,
    double distanceKm,
    int durationMin,
    const QString &intensity,
    const QString &notes,
    bool hiddenFromAthlete,
    const QString &intervalsJson)
{
    setBusy(true);
    if (title.trimmed().isEmpty()) {
        setError(QStringLiteral("Введите название тренировки."));
        setBusy(false);
        return false;
    }
    if (!m_draftDate.isValid()) {
        setError(QStringLiteral("Некорректная дата."));
        setBusy(false);
        return false;
    }
    if (m_selectedAthleteId.isEmpty()) {
        setError(QStringLiteral("Выберите атлета."));
        setBusy(false);
        return false;
    }
    if (!hasAccessToAthlete(m_selectedAthleteId) || !canEditWorkouts()) {
        setError(QStringLiteral("Недостаточно прав для создания тренировки."));
        setBusy(false);
        return false;
    }

    QString intervals;
    if (!validateIntervalsJson(intervalsJson, &intervals)) {
        setBusy(false);
        return false;
    }
    QSqlQuery q(m_db);
    q.prepare(QStringLiteral(
        "INSERT INTO workouts(id, athleteId, date, title, category, distanceKm, durationMin, intensity, notes, hidden, intervalsJson, status, athleteFeedback, athleteMood, perceivedExertion) "
        "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'planned', '', '', 0)"));
    const QString newId = generateId();
    q.addBindValue(newId);
    q.addBindValue(m_selectedAthleteId);
    q.addBindValue(m_draftDate.toString(Qt::ISODate));
    q.addBindValue(title.trimmed());
    q.addBindValue(category);
    q.addBindValue(qMax(0.0, distanceKm));
    q.addBindValue(qMax(0, durationMin));
    q.addBindValue(intensity);
    q.addBindValue(notes.trimmed());
    q.addBindValue(hiddenFromAthlete ? 1 : 0);
    q.addBindValue(intervals);
    if (!q.exec()) {
        setError(QStringLiteral("Ошибка сохранения тренировки: ") + q.lastError().text());
        setBusy(false);
        return false;
    }

    m_selectedDate = m_draftDate;
    m_selectedWorkoutId = newId;

    setCreateDialogOpen(false);
    emit workoutCreated();
    emit selectedDateChanged();
    emit selectedDayChanged();
    emitDataChanged();
    clearError();
    setBusy(false);
    return true;
}

void WorkoutStore::selectWorkout(const QString &id)
{
    if (m_selectedWorkoutId == id)
        return;
    m_selectedWorkoutId = id;
    emit selectedWorkoutChanged();
    emit selectedWorkoutCommentsChanged();
}

bool WorkoutStore::addComment(const QString &author, const QString &text)
{
    if (m_selectedWorkoutId.isEmpty()) {
        setError(QStringLiteral("Сначала выберите тренировку."));
        return false;
    }
    if (text.trimmed().isEmpty()) {
        setError(QStringLiteral("Комментарий пустой."));
        return false;
    }
    const QVariantMap workout = workoutById(m_selectedWorkoutId);
    const QString workoutAthleteId = workout.value(QStringLiteral("athleteId")).toString();
    if (!hasAccessToAthlete(workoutAthleteId)) {
        setError(QStringLiteral("Нет доступа к этой тренировке."));
        return false;
    }
    QSqlQuery q(m_db);
    q.prepare(QStringLiteral(
        "INSERT INTO comments(id, workoutId, author, text, createdAt) VALUES(?, ?, ?, ?, ?)"));
    q.addBindValue(generateId());
    q.addBindValue(m_selectedWorkoutId);
    q.addBindValue(author.trimmed().isEmpty() ? QStringLiteral("coach") : author.trimmed());
    q.addBindValue(text.trimmed());
    q.addBindValue(QDateTime::currentDateTimeUtc().toString(Qt::ISODate));
    if (!q.exec()) {
        setError(QStringLiteral("Ошибка добавления комментария."));
        return false;
    }
    emit selectedWorkoutCommentsChanged();
    clearError();
    return true;
}

bool WorkoutStore::saveTemplate(
    const QString &title,
    const QString &category,
    double distanceKm,
    int durationMin,
    const QString &intensity,
    const QString &intervals,
    const QString &notes,
    const QString &tags)
{
    if (!canEditWorkouts()) {
        setError(QStringLiteral("Только тренер может сохранять шаблоны."));
        return false;
    }
    if (title.trimmed().isEmpty()) {
        setError(QStringLiteral("Введите название шаблона."));
        return false;
    }
    QString intervalsNormalized;
    if (!validateIntervalsJson(intervals, &intervalsNormalized)) {
        return false;
    }
    QSqlQuery q(m_db);
    q.prepare(QStringLiteral(
        "INSERT INTO templates(id, title, category, distanceKm, durationMin, intensity, intervalsJson, notes, tags) "
        "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"));
    q.addBindValue(generateId());
    q.addBindValue(title.trimmed());
    q.addBindValue(category);
    q.addBindValue(qMax(0.0, distanceKm));
    q.addBindValue(qMax(0, durationMin));
    q.addBindValue(intensity);
    q.addBindValue(intervalsNormalized);
    q.addBindValue(notes.trimmed());
    q.addBindValue(tags.trimmed());
    if (!q.exec()) {
        setError(QStringLiteral("Ошибка сохранения шаблона."));
        return false;
    }
    emit templatesChanged();
    clearError();
    return true;
}

bool WorkoutStore::planFromTemplate(const QString &templateId, const QString &dateIso)
{
    const QDate d = QDate::fromString(dateIso, Qt::ISODate);
    if (!d.isValid()) {
        setError(QStringLiteral("Некорректная дата для шаблона."));
        return false;
    }
    if (!canEditWorkouts()) {
        setError(QStringLiteral("Только тренер может планировать по шаблону."));
        return false;
    }
    QSqlQuery q(m_db);
    q.prepare(QStringLiteral(
        "SELECT title, category, distanceKm, durationMin, intensity, intervalsJson, notes "
        "FROM templates WHERE id = ?"));
    q.addBindValue(templateId);
    if (!q.exec() || !q.next()) {
        setError(QStringLiteral("Шаблон не найден."));
        return false;
    }
    m_draftDate = d;
    return createWorkout(
        q.value(0).toString(),
        q.value(1).toString(),
        q.value(2).toDouble(),
        q.value(3).toInt(),
        q.value(4).toString(),
        q.value(6).toString(),
        false,
        q.value(5).toString());
}

bool WorkoutStore::updateWorkout(
    const QString &id,
    const QString &title,
    const QString &category,
    double distanceKm,
    int durationMin,
    const QString &intensity,
    const QString &notes,
    bool hiddenFromAthlete,
    const QString &intervalsJson)
{
    if (id.trimmed().isEmpty()) {
        setError(QStringLiteral("Некорректный идентификатор тренировки."));
        return false;
    }
    if (!hasWriteAccessToWorkout(id)) {
        setError(QStringLiteral("Недостаточно прав для редактирования тренировки."));
        return false;
    }
    if (title.trimmed().isEmpty()) {
        setError(QStringLiteral("Введите название тренировки."));
        return false;
    }
    QString intervalsNormalized;
    if (!validateIntervalsJson(intervalsJson, &intervalsNormalized))
        return false;

    QSqlQuery q(m_db);
    q.prepare(QStringLiteral(
        "UPDATE workouts "
        "SET title = ?, category = ?, distanceKm = ?, durationMin = ?, intensity = ?, notes = ?, hidden = ?, intervalsJson = ? "
        "WHERE id = ?"));
    q.addBindValue(title.trimmed());
    q.addBindValue(category);
    q.addBindValue(qMax(0.0, distanceKm));
    q.addBindValue(qMax(0, durationMin));
    q.addBindValue(intensity);
    q.addBindValue(notes.trimmed());
    q.addBindValue(hiddenFromAthlete ? 1 : 0);
    q.addBindValue(intervalsNormalized);
    q.addBindValue(id);
    if (!q.exec()) {
        setError(QStringLiteral("Ошибка обновления тренировки."));
        return false;
    }
    m_selectedWorkoutId = id;
    emitDataChanged();
    clearError();
    return true;
}

bool WorkoutStore::deleteWorkout(const QString &id)
{
    if (!hasWriteAccessToWorkout(id)) {
        setError(QStringLiteral("Недостаточно прав для удаления тренировки."));
        return false;
    }
    QSqlQuery q(m_db);
    q.prepare(QStringLiteral("DELETE FROM comments WHERE workoutId = ?"));
    q.addBindValue(id);
    q.exec();
    q.prepare(QStringLiteral("DELETE FROM workouts WHERE id = ?"));
    q.addBindValue(id);
    if (!q.exec()) {
        setError(QStringLiteral("Ошибка удаления тренировки."));
        return false;
    }
    if (m_selectedWorkoutId == id)
        m_selectedWorkoutId.clear();
    emitDataChanged();
    clearError();
    return true;
}

bool WorkoutStore::updateTemplate(
    const QString &id,
    const QString &title,
    const QString &category,
    double distanceKm,
    int durationMin,
    const QString &intensity,
    const QString &intervals,
    const QString &notes,
    const QString &tags)
{
    if (!canEditWorkouts()) {
        setError(QStringLiteral("Только тренер может изменять шаблоны."));
        return false;
    }
    if (id.trimmed().isEmpty() || title.trimmed().isEmpty()) {
        setError(QStringLiteral("Проверьте шаблон: id и название обязательны."));
        return false;
    }
    QString intervalsNormalized;
    if (!validateIntervalsJson(intervals, &intervalsNormalized))
        return false;

    QSqlQuery q(m_db);
    q.prepare(QStringLiteral(
        "UPDATE templates "
        "SET title = ?, category = ?, distanceKm = ?, durationMin = ?, intensity = ?, intervalsJson = ?, notes = ?, tags = ? "
        "WHERE id = ?"));
    q.addBindValue(title.trimmed());
    q.addBindValue(category);
    q.addBindValue(qMax(0.0, distanceKm));
    q.addBindValue(qMax(0, durationMin));
    q.addBindValue(intensity);
    q.addBindValue(intervalsNormalized);
    q.addBindValue(notes.trimmed());
    q.addBindValue(tags.trimmed());
    q.addBindValue(id);
    if (!q.exec()) {
        setError(QStringLiteral("Ошибка обновления шаблона."));
        return false;
    }
    emit templatesChanged();
    clearError();
    return true;
}

bool WorkoutStore::deleteTemplate(const QString &id)
{
    if (!canEditWorkouts()) {
        setError(QStringLiteral("Только тренер может удалять шаблоны."));
        return false;
    }
    QSqlQuery q(m_db);
    q.prepare(QStringLiteral("DELETE FROM templates WHERE id = ?"));
    q.addBindValue(id);
    if (!q.exec()) {
        setError(QStringLiteral("Ошибка удаления шаблона."));
        return false;
    }
    emit templatesChanged();
    clearError();
    return true;
}

bool WorkoutStore::markWorkoutStatus(const QString &workoutId, const QString &status, const QString &feedback)
{
    return markWorkoutStatusDetailed(workoutId, status, feedback, QString(), 0);
}

bool WorkoutStore::markWorkoutStatusDetailed(
    const QString &workoutId,
    const QString &status,
    const QString &feedback,
    const QString &mood,
    int perceivedExertion)
{
    const QString normalizedStatus = status.trimmed().toLower();
    if (normalizedStatus != QStringLiteral("planned")
        && normalizedStatus != QStringLiteral("done")
        && normalizedStatus != QStringLiteral("skipped")) {
        setError(QStringLiteral("Некорректный статус тренировки."));
        return false;
    }
    const QVariantMap workout = workoutById(workoutId);
    if (workout.isEmpty()) {
        setError(QStringLiteral("Тренировка не найдена."));
        return false;
    }
    const QString athleteId = workout.value(QStringLiteral("athleteId")).toString();
    if (!hasAccessToAthlete(athleteId)) {
        setError(QStringLiteral("Нет доступа к тренировке."));
        return false;
    }
    if (isAthlete()) {
        QSqlQuery qa(m_db);
        qa.prepare(QStringLiteral("SELECT athleteId FROM users WHERE id = ?"));
        qa.addBindValue(m_currentUserId);
        if (!qa.exec() || !qa.next() || qa.value(0).toString() != athleteId) {
            setError(QStringLiteral("Атлет может менять статус только своих тренировок."));
            return false;
        }
    }
    QString normalizedMood = mood.trimmed();
    int normalizedExertion = qBound(0, perceivedExertion, 6);
    if (normalizedStatus != QStringLiteral("done")) {
        normalizedMood.clear();
        normalizedExertion = 0;
    } else if (normalizedExertion < 1 || normalizedExertion > 6) {
        setError(QStringLiteral("Укажите воспринимаемое усилие от 1 до 6."));
        return false;
    }

    QSqlQuery q(m_db);
    q.prepare(QStringLiteral(
        "UPDATE workouts "
        "SET status = ?, athleteFeedback = ?, athleteMood = ?, perceivedExertion = ? "
        "WHERE id = ?"));
    q.addBindValue(normalizedStatus);
    q.addBindValue(feedback.trimmed());
    q.addBindValue(normalizedMood);
    q.addBindValue(normalizedExertion);
    q.addBindValue(workoutId);
    if (!q.exec()) {
        setError(QStringLiteral("Не удалось обновить статус."));
        return false;
    }
    emitDataChanged();
    clearError();
    return true;
}

bool WorkoutStore::canCurrentUserEditAthlete(const QString &athleteId) const
{
    return isCoach() && hasAccessToAthlete(athleteId);
}

void WorkoutStore::clearError()
{
    if (m_errorMessage.isEmpty())
        return;
    m_errorMessage.clear();
    emit errorChanged(QString());
}

void WorkoutStore::refresh()
{
    emit usersChanged();
    emit currentUserChanged();
    emit athletesChanged();
    emit templatesChanged();
    emitDataChanged();
}

QString WorkoutStore::databasePath() const
{
    const QString baseDir = QStandardPaths::writableLocation(QStandardPaths::AppDataLocation);
    QDir dir(baseDir);
    dir.mkpath(QStringLiteral("."));
    return dir.filePath(QStringLiteral("sport_calendar.sqlite"));
}

QString WorkoutStore::generateId() const
{
    return QString::number(QDateTime::currentMSecsSinceEpoch(), 36)
        + QStringLiteral("_")
        + QString::number(QRandomGenerator::global()->generate(), 16);
}

QVariantMap WorkoutStore::workoutToCardMap(const QVariantMap &w) const
{
    QVariantMap m;
    const QString category = w.value(QStringLiteral("category")).toString();
    const QString intensity = w.value(QStringLiteral("intensity")).toString();
    m.insert(QStringLiteral("id"), w.value(QStringLiteral("id")).toString());
    m.insert(QStringLiteral("title"), w.value(QStringLiteral("title")).toString());
    m.insert(QStringLiteral("category"), category);
    m.insert(QStringLiteral("intensity"), intensity);
    m.insert(QStringLiteral("hidden"), w.value(QStringLiteral("hidden")).toInt() == 1);
    m.insert(QStringLiteral("typeIcon"), categoryIcon(category));
    m.insert(QStringLiteral("typeColor"), categoryColor(category));
    m.insert(QStringLiteral("distance"), QString::number(w.value(QStringLiteral("distanceKm")).toDouble(), 'f', 1) + QStringLiteral(" км"));
    m.insert(QStringLiteral("duration"), QString::number(w.value(QStringLiteral("durationMin")).toInt()) + QStringLiteral(" мин"));
    m.insert(QStringLiteral("status"), w.value(QStringLiteral("status")).toString());
    m.insert(QStringLiteral("athleteFeedback"), w.value(QStringLiteral("athleteFeedback")).toString());
    m.insert(QStringLiteral("athleteMood"), w.value(QStringLiteral("athleteMood")).toString());
    m.insert(QStringLiteral("perceivedExertion"), w.value(QStringLiteral("perceivedExertion")).toInt());

    QString intensityLabel = QStringLiteral("Нормально");
    if (intensity == QStringLiteral("easy"))
        intensityLabel = QStringLiteral("Легко");
    else if (intensity == QStringLiteral("hard"))
        intensityLabel = QStringLiteral("Тяжело");
    else if (intensity == QStringLiteral("moderate"))
        intensityLabel = QStringLiteral("Умеренно");
    m.insert(QStringLiteral("intensityLabel"), intensityLabel);
    m.insert(QStringLiteral("intensityColor"), intensityColor(intensity));
    return m;
}

QVariantMap WorkoutStore::workoutToDetailMap(const QVariantMap &w) const
{
    QVariantMap m = workoutToCardMap(w);
    m.insert(QStringLiteral("notes"), w.value(QStringLiteral("notes")).toString());
    m.insert(QStringLiteral("dateIso"), w.value(QStringLiteral("date")).toString());
    m.insert(QStringLiteral("intervalsJson"), w.value(QStringLiteral("intervalsJson")).toString());
    m.insert(QStringLiteral("athleteId"), w.value(QStringLiteral("athleteId")).toString());
    return m;
}

QString WorkoutStore::categoryIcon(const QString &category) const
{
    if (category == QStringLiteral("bike"))
        return QStringLiteral("[BIKE]");
    if (category == QStringLiteral("swim"))
        return QStringLiteral("[SWIM]");
    return QStringLiteral("[RUN]");
}

QString WorkoutStore::categoryColor(const QString &category) const
{
    if (category == QStringLiteral("bike"))
        return QStringLiteral("#7b1fa2");
    if (category == QStringLiteral("swim"))
        return QStringLiteral("#1e88e5");
    return QStringLiteral("#546e7a");
}

QString WorkoutStore::intensityColor(const QString &intensity) const
{
    if (intensity == QStringLiteral("easy"))
        return QStringLiteral("#43a047");
    if (intensity == QStringLiteral("hard"))
        return QStringLiteral("#e53935");
    return QStringLiteral("#f9a825");
}

QVariantList WorkoutStore::workoutsForDate(const QDate &date) const
{
    QVariantList out;
    QSqlQuery q(m_db);
    QString sql = QStringLiteral(
        "SELECT id, athleteId, date, title, category, distanceKm, durationMin, intensity, notes, hidden, intervalsJson, status, athleteFeedback, athleteMood, perceivedExertion "
        "FROM workouts WHERE athleteId = ? AND date = ?");
    if (isAthlete())
        sql += QStringLiteral(" AND hidden = 0");
    sql += QStringLiteral(" ORDER BY id");
    q.prepare(sql);
    q.addBindValue(m_selectedAthleteId);
    q.addBindValue(date.toString(Qt::ISODate));
    if (!q.exec())
        return out;
    while (q.next()) {
        QVariantMap w;
        w.insert(QStringLiteral("id"), q.value(0).toString());
        w.insert(QStringLiteral("athleteId"), q.value(1).toString());
        w.insert(QStringLiteral("date"), q.value(2).toString());
        w.insert(QStringLiteral("title"), q.value(3).toString());
        w.insert(QStringLiteral("category"), q.value(4).toString());
        w.insert(QStringLiteral("distanceKm"), q.value(5).toDouble());
        w.insert(QStringLiteral("durationMin"), q.value(6).toInt());
        w.insert(QStringLiteral("intensity"), q.value(7).toString());
        w.insert(QStringLiteral("notes"), q.value(8).toString());
        w.insert(QStringLiteral("hidden"), q.value(9).toInt());
        w.insert(QStringLiteral("intervalsJson"), q.value(10).toString());
        w.insert(QStringLiteral("status"), q.value(11).toString());
        w.insert(QStringLiteral("athleteFeedback"), q.value(12).toString());
        w.insert(QStringLiteral("athleteMood"), q.value(13).toString());
        w.insert(QStringLiteral("perceivedExertion"), q.value(14).toInt());
        out.push_back(w);
    }
    return out;
}

QVariantMap WorkoutStore::workoutById(const QString &workoutId) const
{
    if (workoutId.isEmpty())
        return {};
    QSqlQuery q(m_db);
    q.prepare(QStringLiteral(
        "SELECT id, athleteId, date, title, category, distanceKm, durationMin, intensity, notes, hidden, intervalsJson, status, athleteFeedback, athleteMood, perceivedExertion "
        "FROM workouts WHERE id = ?"));
    q.addBindValue(workoutId);
    if (!q.exec() || !q.next())
        return {};
    QVariantMap w;
    w.insert(QStringLiteral("id"), q.value(0).toString());
    w.insert(QStringLiteral("athleteId"), q.value(1).toString());
    w.insert(QStringLiteral("date"), q.value(2).toString());
    w.insert(QStringLiteral("title"), q.value(3).toString());
    w.insert(QStringLiteral("category"), q.value(4).toString());
    w.insert(QStringLiteral("distanceKm"), q.value(5).toDouble());
    w.insert(QStringLiteral("durationMin"), q.value(6).toInt());
    w.insert(QStringLiteral("intensity"), q.value(7).toString());
    w.insert(QStringLiteral("notes"), q.value(8).toString());
    w.insert(QStringLiteral("hidden"), q.value(9).toInt());
    w.insert(QStringLiteral("intervalsJson"), q.value(10).toString());
    w.insert(QStringLiteral("status"), q.value(11).toString());
    w.insert(QStringLiteral("athleteFeedback"), q.value(12).toString());
    w.insert(QStringLiteral("athleteMood"), q.value(13).toString());
    w.insert(QStringLiteral("perceivedExertion"), q.value(14).toInt());
    return w;
}

QVariantList WorkoutStore::commentsForWorkout(const QString &workoutId) const
{
    QVariantList list;
    QSqlQuery q(m_db);
    q.prepare(QStringLiteral(
        "SELECT author, text, createdAt FROM comments WHERE workoutId = ? ORDER BY createdAt"));
    q.addBindValue(workoutId);
    if (!q.exec())
        return list;
    while (q.next()) {
        QVariantMap c;
        c.insert(QStringLiteral("author"), q.value(0).toString());
        c.insert(QStringLiteral("text"), q.value(1).toString());
        c.insert(QStringLiteral("createdAt"), q.value(2).toString());
        list.push_back(c);
    }
    return list;
}

void WorkoutStore::emitDataChanged()
{
    emit selectedDateChanged();
    emit selectedDayChanged();
    emit selectedWorkoutChanged();
    emit selectedWorkoutCommentsChanged();
    emit calendarChanged();
    emit analyticsChanged();
}

bool WorkoutStore::initDatabase()
{
    if (QSqlDatabase::contains(QStringLiteral("qt-calendar-main"))) {
        m_db = QSqlDatabase::database(QStringLiteral("qt-calendar-main"));
    } else {
        m_db = QSqlDatabase::addDatabase(QStringLiteral("QSQLITE"), QStringLiteral("qt-calendar-main"));
        m_db.setDatabaseName(databasePath());
    }
    if (!m_db.open()) {
        setError(QStringLiteral("Не удалось открыть БД: ") + m_db.lastError().text());
        return false;
    }
    return ensureSchema();
}

bool WorkoutStore::ensureSchema()
{
    QSqlQuery q(m_db);
    if (!q.exec(QStringLiteral(
            "CREATE TABLE IF NOT EXISTS users("
            "id TEXT PRIMARY KEY,"
            "name TEXT NOT NULL,"
            "role TEXT NOT NULL,"
            "athleteId TEXT)"))) {
        setError(QStringLiteral("Ошибка схемы users: ") + q.lastError().text());
        return false;
    }

    if (!q.exec(QStringLiteral("CREATE TABLE IF NOT EXISTS athletes(id TEXT PRIMARY KEY, name TEXT NOT NULL)"))) {
        setError(QStringLiteral("Ошибка схемы athletes: ") + q.lastError().text());
        return false;
    }

    if (!q.exec(QStringLiteral(
            "CREATE TABLE IF NOT EXISTS coach_athlete_links("
            "coachUserId TEXT NOT NULL,"
            "athleteId TEXT NOT NULL,"
            "PRIMARY KEY(coachUserId, athleteId))"))) {
        setError(QStringLiteral("Ошибка схемы coach_athlete_links: ") + q.lastError().text());
        return false;
    }

    if (!q.exec(QStringLiteral(
            "CREATE TABLE IF NOT EXISTS workouts("
            "id TEXT PRIMARY KEY,"
            "athleteId TEXT NOT NULL,"
            "date TEXT NOT NULL,"
            "title TEXT NOT NULL,"
            "category TEXT NOT NULL,"
            "distanceKm REAL NOT NULL,"
            "durationMin INTEGER NOT NULL,"
            "intensity TEXT NOT NULL,"
            "notes TEXT,"
            "hidden INTEGER NOT NULL DEFAULT 0,"
            "intervalsJson TEXT NOT NULL DEFAULT '[]',"
            "status TEXT NOT NULL DEFAULT 'planned',"
            "athleteFeedback TEXT NOT NULL DEFAULT '',"
            "athleteMood TEXT NOT NULL DEFAULT '',"
            "perceivedExertion INTEGER NOT NULL DEFAULT 0)"))) {
        setError(QStringLiteral("Ошибка схемы workouts: ") + q.lastError().text());
        return false;
    }

    if (!q.exec(QStringLiteral(
            "CREATE TABLE IF NOT EXISTS comments("
            "id TEXT PRIMARY KEY,"
            "workoutId TEXT NOT NULL,"
            "author TEXT NOT NULL,"
            "text TEXT NOT NULL,"
            "createdAt TEXT NOT NULL)"))) {
        setError(QStringLiteral("Ошибка схемы comments: ") + q.lastError().text());
        return false;
    }

    if (!q.exec(QStringLiteral(
            "CREATE TABLE IF NOT EXISTS templates("
            "id TEXT PRIMARY KEY,"
            "title TEXT NOT NULL,"
            "category TEXT NOT NULL,"
            "distanceKm REAL NOT NULL,"
            "durationMin INTEGER NOT NULL,"
            "intensity TEXT NOT NULL,"
            "intervalsJson TEXT NOT NULL,"
            "notes TEXT,"
            "tags TEXT)"))) {
        setError(QStringLiteral("Ошибка схемы templates: ") + q.lastError().text());
        return false;
    }

    // Backward-compatible migration for older schemas.
    q.exec(QStringLiteral("ALTER TABLE workouts ADD COLUMN status TEXT NOT NULL DEFAULT 'planned'"));
    q.exec(QStringLiteral("ALTER TABLE workouts ADD COLUMN athleteFeedback TEXT NOT NULL DEFAULT ''"));
    q.exec(QStringLiteral("ALTER TABLE workouts ADD COLUMN athleteMood TEXT NOT NULL DEFAULT ''"));
    q.exec(QStringLiteral("ALTER TABLE workouts ADD COLUMN perceivedExertion INTEGER NOT NULL DEFAULT 0"));

    return true;
}

void WorkoutStore::seedDatabase()
{
    QSqlQuery q(m_db);
    q.exec(QStringLiteral("INSERT OR IGNORE INTO athletes(id,name) VALUES('ath1','Иван Петров')"));
    q.exec(QStringLiteral("INSERT OR IGNORE INTO athletes(id,name) VALUES('ath2','Анна Смирнова')"));

    q.exec(QStringLiteral(
        "INSERT OR IGNORE INTO users(id,name,role,athleteId) VALUES('coach1','Главный тренер','coach',NULL)"));
    q.exec(QStringLiteral(
        "INSERT OR IGNORE INTO users(id,name,role,athleteId) VALUES('athlete_user_1','Иван Петров','athlete','ath1')"));
    q.exec(QStringLiteral(
        "INSERT OR IGNORE INTO users(id,name,role,athleteId) VALUES('athlete_user_2','Анна Смирнова','athlete','ath2')"));

    q.exec(QStringLiteral("INSERT OR IGNORE INTO coach_athlete_links(coachUserId,athleteId) VALUES('coach1','ath1')"));
    q.exec(QStringLiteral("INSERT OR IGNORE INTO coach_athlete_links(coachUserId,athleteId) VALUES('coach1','ath2')"));

    m_currentUserId = QStringLiteral("coach1");
    m_selectedAthleteId = QStringLiteral("ath1");

    q.prepare(QStringLiteral("SELECT COUNT(*) FROM workouts"));
    if (q.exec() && q.next() && q.value(0).toInt() == 0) {
        m_draftDate = QDate::currentDate().addDays(-2);
        createWorkout(QStringLiteral("Бег - Восстановительный кросс"), QStringLiteral("run"), 3.0, 15, QStringLiteral("easy"), QStringLiteral("Темп: 5:00/км"), false, QStringLiteral("[{\"step\":\"15min easy\"}]"));
        m_draftDate = QDate::currentDate().addDays(-2);
        createWorkout(QStringLiteral("Плавание - Выносливость"), QStringLiteral("swim"), 0.5, 10, QStringLiteral("moderate"), QStringLiteral("Темп: 2:00/100м"), false, QStringLiteral("[{\"step\":\"10x50m\"}]"));
        m_draftDate = QDate::currentDate().addDays(-1);
        createWorkout(QStringLiteral("Бег - Длительный бег"), QStringLiteral("run"), 8.0, 45, QStringLiteral("moderate"), QStringLiteral("Пульс: 145"), false, QStringLiteral("[{\"step\":\"45min aerobic\"}]"));
    }

    q.prepare(QStringLiteral("SELECT COUNT(*) FROM templates"));
    if (q.exec() && q.next() && q.value(0).toInt() == 0) {
        q.exec(QStringLiteral(
            "INSERT INTO templates(id,title,category,distanceKm,durationMin,intensity,intervalsJson,notes,tags) "
            "VALUES('tpl1','Интервалы 8x400','run',8,55,'hard','[{\"step\":\"10min warmup\"},{\"step\":\"8x400\"}]','Работа над скоростью','run,interval')"));
        q.exec(QStringLiteral(
            "INSERT INTO templates(id,title,category,distanceKm,durationMin,intensity,intervalsJson,notes,tags) "
            "VALUES('tpl2','Велостанок sweet spot','bike',35,70,'moderate','[{\"step\":\"3x12min sweet spot\"}]','Контроль мощности','bike,power')"));
    }

    m_selectedDate = QDate::currentDate();
    m_monthStart = QDate(m_selectedDate.year(), m_selectedDate.month(), 1);
    emit usersChanged();
    emit currentUserChanged();
    emit athletesChanged();
    emit templatesChanged();
    emitDataChanged();
}

bool WorkoutStore::validateIntervalsJson(const QString &intervalsJson, QString *normalized) const
{
    const QString trimmed = intervalsJson.trimmed();
    if (trimmed.isEmpty()) {
        if (normalized)
            *normalized = QStringLiteral("[]");
        return true;
    }
    QJsonParseError error;
    const QJsonDocument json = QJsonDocument::fromJson(trimmed.toUtf8(), &error);
    if (error.error != QJsonParseError::NoError || !json.isArray()) {
        const_cast<WorkoutStore *>(this)->setError(QStringLiteral("Интервалы должны быть JSON-массивом."));
        return false;
    }
    if (normalized)
        *normalized = QString::fromUtf8(json.toJson(QJsonDocument::Compact));
    return true;
}

bool WorkoutStore::isCoach() const
{
    return currentUserRole() == QStringLiteral("coach");
}

bool WorkoutStore::isAthlete() const
{
    return currentUserRole() == QStringLiteral("athlete");
}

bool WorkoutStore::hasAccessToAthlete(const QString &athleteId) const
{
    if (athleteId.trimmed().isEmpty())
        return false;
    if (isCoach()) {
        QSqlQuery q(m_db);
        q.prepare(QStringLiteral("SELECT COUNT(*) FROM coach_athlete_links WHERE coachUserId = ? AND athleteId = ?"));
        q.addBindValue(m_currentUserId);
        q.addBindValue(athleteId);
        return q.exec() && q.next() && q.value(0).toInt() > 0;
    }
    if (isAthlete()) {
        QSqlQuery q(m_db);
        q.prepare(QStringLiteral("SELECT athleteId FROM users WHERE id = ?"));
        q.addBindValue(m_currentUserId);
        return q.exec() && q.next() && q.value(0).toString() == athleteId;
    }
    return false;
}

bool WorkoutStore::hasWriteAccessToWorkout(const QString &workoutId) const
{
    if (!canEditWorkouts())
        return false;
    const QVariantMap workout = workoutById(workoutId);
    if (workout.isEmpty())
        return false;
    return hasAccessToAthlete(workout.value(QStringLiteral("athleteId")).toString());
}

void WorkoutStore::setError(const QString &message)
{
    m_errorMessage = message;
    emit errorChanged(message);
}

void WorkoutStore::setBusy(bool value)
{
    if (m_busy == value)
        return;
    m_busy = value;
    emit busyChanged();
}

