from mage_ai.api.resources.GenericResource import GenericResource
from mage_ai.data_preparation.git import Git
from mage_ai.data_preparation.preferences import get_preferences
from mage_ai.data_preparation.sync import GitConfig


class SyncResource(GenericResource):
    @classmethod
    def collection(self, query, meta, user, **kwargs):
        preferences = get_preferences()
        sync_config = preferences.sync_config
        return self.build_result_set(
            [sync_config],
            user,
            **kwargs,
        )

    @classmethod
    def create(self, payload, user, **kwargs):
        sync_config = GitConfig.load(config=payload)
        get_preferences().update_preferences(
            dict(sync_config=sync_config.to_dict())
        )

        Git(sync_config)

        return self(get_preferences().sync_config, user, **kwargs)

    @classmethod
    def member(self, pk, user, **kwargs):
        return self(get_preferences().sync_config, user, **kwargs)

    def update(self, payload, **kwargs):
        git_manager = Git.get_manager()
        config = git_manager.git_config
        action_type = payload.get('action_type')
        if action_type == 'sync_data':
            git_manager.check_connection()
            git_manager.reset(config.branch)

        return self
