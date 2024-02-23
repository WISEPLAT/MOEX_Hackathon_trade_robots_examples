class BuildIndexJob
  include Sidekiq::Job

  def perform(id)
    if (custom_index = CustomIndex.find(id))
      begin
        IndexCalculator.build_index(custom_index)
      rescue StandardError => e
        custom_index.update!(status: "done", error: e.message)
      end
    end
  end
end
