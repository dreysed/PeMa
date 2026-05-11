#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include <QQuickStyle>

#include "backend/WorkoutStore.h"

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);
    app.setApplicationName(QStringLiteral("Qt Calendar App"));
    app.setOrganizationName(QStringLiteral("SportApp"));

    QQuickStyle::setStyle(QStringLiteral("Fusion"));

    WorkoutStore store;
    QQmlApplicationEngine engine;
    engine.rootContext()->setContextProperty(QStringLiteral("workoutStore"), &store);

    const QUrl url(QStringLiteral("qrc:/qml/main.qml"));
    QObject::connect(
        &engine,
        &QQmlApplicationEngine::objectCreated,
        &app,
        [url](QObject *obj, const QUrl &objUrl) {
            if (!obj && url == objUrl)
                QCoreApplication::exit(-1);
        },
        Qt::QueuedConnection
    );

    engine.load(url);
    return app.exec();
}

